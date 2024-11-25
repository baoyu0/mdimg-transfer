"""
处理 Markdown 文件的路由
"""
import os
import aiofiles
from pathlib import Path
from quart import Blueprint, request, jsonify, current_app, make_response
from .config import config
from test_download import process_markdown_file
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tempfile
import aiohttp
import time

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/process', methods=['POST'])
async def process_file():
    """处理上传的 Markdown 文件"""
    try:
        # 获取上传的文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
            
        file = request.files['file']
        if not file.filename:
            return jsonify({'error': '文件名为空'}), 400
            
        # 保存上传的文件
        input_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
        await file.save(input_path)
        
        # 生成输出文件路径
        output_filename = f"processed_{file.filename}"
        output_path = os.path.join(config.PROCESSED_FOLDER, output_filename)
        image_dir = os.path.join(config.IMAGE_FOLDER, os.path.splitext(file.filename)[0])
        
        # 处理文件
        total_images, success_count = await process_markdown_file(input_path, output_path, image_dir)
        
        return jsonify({
            'message': '处理成功',
            'total_images': total_images,
            'success_count': success_count,
            'output_file': output_path,
            'image_dir': image_dir
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/convert-html', methods=['POST'])
async def convert_html():
    """将HTML页面转换为Markdown并处理其中的图片"""
    try:
        data = await request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': '请提供网页URL'}), 400
            
        url = data['url']
        
        # 获取HTML内容并转换为Markdown
        html_content, title = await current_app.html_converter.fetch_html(url)
        markdown_content = current_app.html_converter.convert_to_markdown(html_content)
        
        # 生成临时Markdown文件
        safe_title = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_')).strip()
        temp_filename = f"{safe_title[:50]}.md"
        input_path = os.path.join(config.TEMP_DIR, temp_filename)
        
        # 保存Markdown内容到临时文件
        async with aiofiles.open(input_path, 'w', encoding='utf-8') as f:
            await f.write(markdown_content)
        
        # 处理Markdown文件（包括下载和上传图片）
        output_filename = f"processed_{temp_filename}"
        output_path = os.path.join(config.PROCESSED_FOLDER, output_filename)
        image_dir = os.path.join(config.IMAGE_FOLDER, Path(temp_filename).stem)
        
        total_images, success_count = await process_markdown_file(input_path, output_path, image_dir)
        
        # 读取处理后的文件内容
        async with aiofiles.open(output_path, 'r', encoding='utf-8') as f:
            processed_content = await f.read()
        
        # 清理临时文件
        os.remove(input_path)
        
        return jsonify({
            'message': '转换成功',
            'title': title,
            'total_images': total_images,
            'success_count': success_count,
            'content': processed_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/process-url', methods=['POST'])
async def process_url():
    try:
        data = await request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # 创建临时目录用于处理文件
        with tempfile.TemporaryDirectory() as temp_dir:
            # 下载URL内容
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return jsonify({'error': f'Failed to fetch URL: {response.status}'}), 400
                    content = await response.text()

            # 解析HTML并提取图片链接
            soup = BeautifulSoup(content, 'html.parser')
            images = soup.find_all('img')
            
            # 收集图片信息
            image_data = []
            for img in images:
                src = img.get('src', '')
                if src:
                    if not src.startswith(('http://', 'https://')):
                        # 处理相对URL
                        src = urljoin(url, src)
                    image_data.append({
                        'original_url': src,
                        'filename': os.path.basename(urlparse(src).path) or 'image.jpg'
                    })

            # 创建Markdown文件
            md_content = f"# Images from {url}\n\n"
            for img in image_data:
                md_content += f"![{img['filename']}]({img['original_url']})\n\n"

            # 保存处理后的文件
            processed_filename = f"processed_{int(time.time())}.md"
            output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], processed_filename)
            
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                await f.write(md_content)

            return jsonify({
                'message': 'URL processed successfully',
                'processed_filename': processed_filename,
                'original_url': url,
                'image_count': len(image_data),
                'download_url': f"/api/download/{processed_filename}"
            })

    except Exception as e:
        current_app.logger.error(f"Error processing URL: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/download/<filename>')
async def download_file(filename):
    """下载处理后的文件"""
    try:
        file_path = os.path.join(current_app.config['PROCESSED_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '文件未找到'}), 404

        async def send_file():
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
                return content

        response = await make_response(send_file())
        response.headers['Content-Type'] = 'text/markdown; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        current_app.logger.error(f"下载文件时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500
