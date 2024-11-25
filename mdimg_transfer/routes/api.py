"""
API 路由模块。
提供文件上传和处理的 API 端点。
"""

import os
import uuid
import logging
import asyncio
from quart import Blueprint, request, jsonify, websocket, current_app, send_from_directory
from werkzeug.utils import secure_filename
from ..services.file_processor import FileProcessor
from ..services.url_processor import UrlProcessor
from ..services.progress import ProgressManager
from ..config import Config

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')
progress_manager = ProgressManager()

@bp.websocket('/ws/progress/<task_id>')
async def progress_ws(task_id):
    """WebSocket endpoint for progress updates"""
    try:
        while True:
            progress = progress_manager.get_progress(task_id)
            if progress:
                await websocket.send_json(progress)
                if progress.get('status') in ['completed', 'error']:
                    break
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

@bp.route('/process', methods=['POST'])
async def process_markdown():
    """处理 Markdown 文件"""
    try:
        files = await request.files
        if 'file' not in files:
            return jsonify({"error": "No file provided"}), 400
        
        file = files['file']
        if not file.filename:
            return jsonify({"error": "No file selected"}), 400
            
        if not file.filename.lower().endswith('.md'):
            return jsonify({"error": "Invalid file type. Please upload a Markdown file."}), 400
            
        task_id = progress_manager.create_task()
        
        def progress_update(msg):
            progress_manager.update_progress(
                task_id, 
                msg.get('message', ''), 
                msg.get('progress', 0), 
                msg.get('details', {})
            )
        
        # 处理文件
        processor = FileProcessor(current_app.config)
        result = await processor.process_markdown_file(
            file=file,
            task_id=task_id,
            progress_callback=progress_update
        )
        
        if result.get('error'):
            progress_manager.set_error(task_id, result['error'])
            return jsonify({'error': result['error']}), 400
            
        progress_manager.set_completed(task_id)
        return jsonify({
            'task_id': task_id,
            'download_url': result['download_url'],
            'total_images': result['total_images'],
            'successful_downloads': result['successful_downloads']
        })

    except Exception as e:
        logger.error(f"Error processing markdown: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/process-url', methods=['POST'])
async def process_url():
    """处理URL请求"""
    try:
        data = await request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data['url']
        task_id = progress_manager.create_task()
        
        def progress_update(msg):
            progress_manager.update_progress(
                task_id, 
                msg.get('message', ''), 
                msg.get('progress', 0), 
                msg.get('details', {})
            )
        
        # 处理URL
        processor = UrlProcessor(current_app.config)
        result = await processor.process_url(
            url=url,
            task_id=task_id,
            progress_callback=progress_update
        )
        
        if result.get('error'):
            progress_manager.set_error(task_id, result['error'])
            return jsonify({'error': result['error']}), 400
            
        progress_manager.set_completed(task_id)
        return jsonify({
            'task_id': task_id,
            'download_url': result['download_url'],
            'total_images': result['total_images'],
            'successful_downloads': result['successful_downloads']
        })

    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/download/<filename>')
async def download_file(filename):
    """下载处理后的文件"""
    try:
        return await send_from_directory(
            current_app.config['PROCESSED_DIR'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({"error": "File not found"}), 404
