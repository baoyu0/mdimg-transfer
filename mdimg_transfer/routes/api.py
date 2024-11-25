"""
API 路由模块。
提供文件上传和处理的 API 端点。
"""

import os
import logging
import aiofiles
from quart import Blueprint, request, jsonify, current_app, send_file
from ..core.markdown_processor import MarkdownProcessor
from ..core.image_downloader import ImageDownloader
from ..core.r2_uploader import R2Uploader
from pathlib import Path
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from ..config import config

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')

# 创建必要的实例
downloader = ImageDownloader()
r2_uploader = R2Uploader()
markdown_processor = MarkdownProcessor(downloader=downloader, r2_uploader=r2_uploader)

@bp.route('/process', methods=['POST'])
async def process_markdown():
    """
    处理 Markdown 文件。
    包括：解析图片链接、下载图片、处理图片、上传到新位置、更新文档。
    """
    try:
        files = await request.files
        if 'file' not in files:
            return jsonify({
                "error": "No file provided"
            }), 400
        
        file = files['file']
        if not file.filename:
            return jsonify({
                "error": "No file selected"
            }), 400
            
        # 确保文件名安全
        filename = secure_filename(file.filename)
        
        # 保存上传的文件
        temp_path = os.path.join(config.UPLOAD_FOLDER, filename)
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        await file.save(temp_path)
        
        # 读取文件内容
        async with aiofiles.open(temp_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
            
        # 删除临时文件
        os.remove(temp_path)
        
        if not content:
            return jsonify({
                "error": "Empty file"
            }), 400
        
        logger.info("收到处理请求，Markdown文本长度: %s", len(content))
        
        # 处理 Markdown 文件
        logger.info("开始处理Markdown文本...")
        new_content, download_results = await markdown_processor.process_content(content)
        
        # 统计成功下载的图片数量
        successful_downloads = sum(1 for result in download_results.values() if isinstance(result, tuple) and result[0])
        
        logger.info("处理完成！处理了 %s 个链接，成功下载 %s 个图片", len(markdown_processor.image_links), successful_downloads)
        
        if download_results:
            logger.info("下载失败的图片:")
            for url, result in download_results.items():
                if not isinstance(result, tuple) or not result[0]:
                    logger.info("- %s", url)
                    
        # Check for errors in markdown processor
        if hasattr(markdown_processor, 'errors') and markdown_processor.errors:
            logger.info("处理过程中的错误:")
            for error in markdown_processor.errors:
                logger.info("- %s", error)
        
        # 保存处理后的文件
        processed_filename = f"processed_{filename}"
        processed_path = os.path.join(config.PROCESSED_FOLDER, processed_filename)
        
        # 确保目录存在
        os.makedirs(config.PROCESSED_FOLDER, exist_ok=True)
        
        # 写入处理后的内容
        async with aiofiles.open(processed_path, mode='w', encoding='utf-8') as f:
            await f.write(new_content)
        
        return jsonify({
            "message": "File processed successfully",
            "original_filename": filename,
            "processed_filename": processed_filename,
            "total_images": len(markdown_processor.image_links),
            "successful_downloads": successful_downloads,
            "download_url": f"/api/download/{processed_filename}"
        })
        
    except Exception as e:
        logger.error("处理过程中发生错误: %s", str(e), exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@bp.route('/download/<filename>')
async def download_file(filename):
    """下载处理后的文件"""
    try:
        file_path = os.path.join(config.PROCESSED_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({
                "error": "File not found"
            }), 404
        
        # 读取文件内容
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
            
        # 设置响应头
        headers = {
            'Content-Type': 'text/markdown',
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        # 返回文件内容
        return content, 200, headers
        
    except Exception as e:
        logger.error("Error downloading file: %s", str(e), exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@bp.route('/images/<filename>')
async def serve_image(filename):
    """提供图片文件"""
    try:
        file_path = os.path.join(config.IMAGE_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({
                "error": "Image not found"
            }), 404
        
        return await send_file(file_path)
    except Exception as e:
        logger.error("Error serving image: %s", str(e), exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@bp.route('/process_url', methods=['POST'])
async def process_url():
    """
    处理网页URL。
    提取网页内容，转换为Markdown格式，并处理其中的图片。
    """
    try:
        data = await request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                "error": "No URL provided"
            }), 400

        url = data['url']
        if not url:
            return jsonify({
                "error": "Empty URL"
            }), 400

        try:
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return jsonify({
                    "error": "Invalid URL format"
                }), 400
        except Exception:
            return jsonify({
                "error": "Invalid URL"
            }), 400

        # 生成一个唯一的文件名
        filename = f"url_{secure_filename(url)}.md"
        temp_path = os.path.join(config.UPLOAD_FOLDER, filename)
        
        try:
            # 下载并处理URL内容
            content = await downloader.download_url_content(url)
            if not content:
                return jsonify({
                    "error": "Failed to fetch URL content"
                }), 400

            # 保存为临时文件
            async with aiofiles.open(temp_path, 'w', encoding='utf-8') as f:
                await f.write(content)

            # 处理文件中的图片
            processed_path = await markdown_processor.process_file(temp_path)
            if not processed_path:
                return jsonify({
                    "error": "Failed to process content"
                }), 500

            return jsonify({
                "success": True,
                "download_id": os.path.basename(processed_path)
            })

        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            return jsonify({
                "error": f"Failed to process URL: {str(e)}"
            }), 500

    except Exception as e:
        logger.error(f"Error in process_url: {str(e)}")
        return jsonify({
            "error": "Internal server error"
        }), 500
