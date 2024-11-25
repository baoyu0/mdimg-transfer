import os
import logging
import uuid
from quart import Quart, request, jsonify, websocket, send_file, render_template
from prometheus_client import start_http_server, CONTENT_TYPE_LATEST, generate_latest
from .markdown_processor import process_markdown_async
from .core import ImageProcessor, ImageConfig, ProcessingHistory, init_db, get_session_factory, get_session
from .core import manager as websocket_manager
import boto3
import tempfile
import asyncio
from typing import List, Dict

app = Quart(__name__, static_folder='../static', template_folder='../templates')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# 配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///mdimg.db')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
PUBLIC_URL = os.getenv('PUBLIC_URL')

@app.route('/')
async def index():
    """主页"""
    return await render_template('index.html')

# 初始化S3客户端
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 任务状态管理
task_status: Dict[str, Dict] = {}

@app.before_serving
async def startup():
    """启动时初始化"""
    # 初始化数据库引擎
    app.db_engine = await init_db(DATABASE_URL)
    # 创建会话工厂
    app.session_factory = get_session_factory(app.db_engine)
    # 启动Prometheus指标服务器
    start_http_server(9090)

@app.route('/metrics')
async def metrics():
    """导出处理指标"""
    try:
        async with get_session(app.session_factory) as session:
            # 获取总处理数
            total_stmt = select(ProcessingHistory)
            total_result = await session.execute(total_stmt)
            total_processed = len(total_result.scalars().all())
            
            # 获取成功数
            success_stmt = select(ProcessingHistory).where(ProcessingHistory.status == 'success')
            success_result = await session.execute(success_stmt)
            success_count = len(success_result.scalars().all())
            
            # 计算成功率和平均处理时间
            success_rate = (success_count / total_processed * 100) if total_processed > 0 else 0
            
            # 获取平均处理时间
            time_stmt = select(ProcessingHistory.processing_time).where(ProcessingHistory.status == 'success')
            time_result = await session.execute(time_stmt)
            processing_times = [t for t in time_result.scalars() if t is not None]
            avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
            
            return jsonify({
                'total_processed': total_processed,
                'success_rate': success_rate,
                'average_processing_time': avg_time
            })
            
    except Exception as e:
        logger.error(f"获取指标时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.websocket('/ws/<client_id>')
async def ws(client_id: str):
    """WebSocket连接处理"""
    try:
        current_ws = websocket._get_current_object()
        await websocket_manager.connect(current_ws, client_id)
        while True:
            try:
                data = await current_ws.receive_json()
                task_id = data.get('task_id')
                if task_id:
                    websocket_manager.register_task(task_id, client_id)
            except Exception:
                break
    finally:
        websocket_manager.disconnect(client_id)

async def process_file(file, temp_dir: str, session, task_id: str):
    """处理单个文件并更新进度"""
    try:
        temp_file = os.path.join(temp_dir, file.filename)
        await file.save(temp_file)
        
        # 创建图片处理器
        processor = ImageProcessor(
            cache_dir=os.path.join(temp_dir, 'cache')
        )
        
        # 处理Markdown文件
        results = await process_markdown_async(
            temp_file,
            temp_dir,
            session,
            s3_client,
            BUCKET_NAME,
            PUBLIC_URL,
            processor
        )
        
        return {
            'filename': file.filename,
            'status': 'success',
            'results': results
        }
    except Exception as e:
        logger.error(f"处理文件 {file.filename} 时出错: {str(e)}")
        return {
            'filename': file.filename,
            'status': 'error',
            'error': str(e)
        }

@app.route('/process', methods=['POST'])
async def process_markdown():
    """处理Markdown文件(支持批量)"""
    try:
        files = await request.files
        if not files:
            return jsonify({'error': '没有上传文件'}), 400
        
        # 生成任务ID
        task_id = str(uuid.uuid4())
        task_status[task_id] = {
            'total': len(files),
            'processed': 0,
            'results': []
        }
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            async with get_session(app.session_factory) as session:
                tasks = []
                for file in files.values():
                    if not file.filename.endswith('.md'):
                        continue
                    
                    # 更新进度
                    task_status[task_id]['processed'] += 1
                    progress = {
                        'task_id': task_id,
                        'type': 'progress',
                        'current': task_status[task_id]['processed'],
                        'total': task_status[task_id]['total'],
                        'filename': file.filename
                    }
                    await websocket_manager.broadcast_progress(task_id, progress)
                    
                    # 处理文件
                    result = await process_file(file, temp_dir, session, task_id)
                    task_status[task_id]['results'].append(result)
                    
                    # 发送处理结果
                    await websocket_manager.broadcast_progress(task_id, {
                        'task_id': task_id,
                        'type': 'result',
                        'result': result
                    })
                
                return jsonify({
                    'task_id': task_id,
                    'message': '处理完成',
                    'results': task_status[task_id]['results']
                }), 200
                
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/task/<task_id>')
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in task_status:
        return jsonify({'error': '任务不存在'}), 404
    return jsonify(task_status[task_id])

@app.route('/history')
async def get_history():
    """获取处理历史记录"""
    try:
        async with get_session(app.session_factory) as session:
            stmt = select(ProcessingHistory).order_by(ProcessingHistory.created_at.desc())
            result = await session.execute(stmt)
            history = result.scalars().all()
            
            return jsonify([{
                'id': h.id,
                'original_url': h.original_url,
                'processed_url': h.processed_url,
                'file_size_before': h.file_size_before,
                'file_size_after': h.file_size_after,
                'mime_type': h.mime_type,
                'status': h.status,
                'error_message': h.error_message,
                'created_at': h.created_at.isoformat() if h.created_at else None,
                'processing_time': h.processing_time
            } for h in history])
            
    except Exception as e:
        logger.error(f"获取历史记录时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
async def get_stats():
    """获取处理统计信息"""
    try:
        async with get_session(app.session_factory) as session:
            # 获取总图片数
            total_stmt = select(ProcessingHistory)
            total_result = await session.execute(total_stmt)
            total_images = len(total_result.scalars().all())
            
            # 获取成功和失败数
            success_stmt = select(ProcessingHistory).where(ProcessingHistory.status == 'success')
            success_result = await session.execute(success_stmt)
            success_count = len(success_result.scalars().all())
            
            failure_stmt = select(ProcessingHistory).where(ProcessingHistory.status == 'failed')
            failure_result = await session.execute(failure_stmt)
            failure_count = len(failure_result.scalars().all())
            
            # 获取总处理大小
            size_stmt = select(ProcessingHistory.file_size_before).where(ProcessingHistory.status == 'success')
            size_result = await session.execute(size_stmt)
            total_size = sum([s for s in size_result.scalars() if s is not None])
            
            return jsonify({
                'total_images': total_images,
                'success_count': success_count,
                'failure_count': failure_count,
                'total_size': total_size
            })
            
    except Exception as e:
        logger.error(f"获取统计信息时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
