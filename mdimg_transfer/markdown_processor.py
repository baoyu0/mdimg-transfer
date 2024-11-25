"""Markdown文件处理模块"""

import re
import os
import logging
import asyncio
import hashlib
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, unquote
from .core import ImageProcessor, ImageConfig
from .errors import ValidationError, ProcessingError
from .models import ProcessingHistory

logger = logging.getLogger(__name__)

# Markdown图片链接的正则表达式
MD_IMAGE_PATTERN = r'!\[(.*?)\]\((.*?)\)'

def is_svg_content(url: str) -> bool:
    """检查是否是SVG内容
    
    Args:
        url: 要检查的内容
        
    Returns:
        bool: 是否是SVG内容
    """
    svg_markers = [
        'xmlns=',
        '<svg',
        '</svg>',
        'stroke=',
        'viewBox=',
    ]
    return any(marker in url for marker in svg_markers)

def is_placeholder_svg(content: str) -> bool:
    """检查是否是占位SVG图片
    
    Args:
        content: SVG内容
        
    Returns:
        bool: 是否是占位图片
    """
    # 检查是否是1x1像素的空白SVG
    placeholder_markers = [
        'width=\'1\' height=\'1\'',
        'width="1" height="1"',
        'fill-opacity=\'0\'',
        'fill-opacity="0"',
        'transform=\'translate(-249.000000, -126.000000)\'',  # 微信常用的占位图变换
    ]
    return any(marker in content for marker in placeholder_markers)

def is_valid_image_url(url: str) -> Tuple[bool, str]:
    """验证URL是否是有效的图片URL
    
    Args:
        url: 要验证的URL
        
    Returns:
        Tuple[bool, str]: (是否是有效URL, URL类型['image', 'svg', 'invalid'])
    """
    # 检查是否是SVG内容
    if is_svg_content(url):
        # 如果是占位SVG，跳过
        if is_placeholder_svg(url):
            return False, 'invalid'
        return True, 'svg'
        
    try:
        # 解析URL
        parsed = urlparse(url)
        
        # 检查scheme
        if not parsed.scheme or parsed.scheme not in ('http', 'https'):
            return False, 'invalid'
            
        # 检查域名
        valid_domains = ['mmbiz.qpic.cn', 'res.wx.qq.com']
        if not any(domain in parsed.netloc for domain in valid_domains):
            # 如果是其他域名的SVG，也认为是有效的
            if url.lower().endswith('.svg'):
                # 检查是否是微信的占位图URL
                if 'www.w3.org/2000/svg' in url and 'width=1' in url:
                    return False, 'invalid'
                return True, 'svg'
            return False, 'invalid'
            
        # 检查路径
        if not parsed.path or parsed.path == '/':
            return False, 'invalid'
            
        return True, 'image'
        
    except Exception:
        return False, 'invalid'

def save_svg_content(content: str, temp_dir: str) -> str:
    """保存SVG内容到文件
    
    Args:
        content: SVG内容
        temp_dir: 临时目录
        
    Returns:
        str: 保存的文件路径
    """
    # 生成文件名
    content_hash = hashlib.md5(content.encode()).hexdigest()
    filename = f"svg_{content_hash}.svg"
    filepath = os.path.join(temp_dir, filename)
    
    # 如果内容不是完整的SVG，添加必要的标签
    if not content.strip().startswith('<?xml'):
        content = f'<?xml version="1.0" encoding="UTF-8"?>\n{content}'
    if not content.strip().startswith('<svg'):
        content = f'<svg xmlns="http://www.w3.org/2000/svg">\n{content}\n</svg>'
        
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return filepath

async def process_markdown_async(
    file_path: str,
    temp_dir: str,
    session,
    s3_client,
    bucket_name: str,
    public_url: str,
    image_processor: ImageProcessor
) -> Dict[str, any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = re.finditer(MD_IMAGE_PATTERN, content)
        replacements = []
        stats = {
            'total_images': 0,
            'processed_images': 0,
            'failed_images': 0,
            'skipped_placeholders': 0,
            'total_size_before': 0,
            'total_size_after': 0,
            'svg_images': 0
        }
        
        config = ImageConfig(
            max_file_size=50 * 1024 * 1024,
            quality=85,
            max_width=1920,
            max_height=1080,
            strip_metadata=True,
            progressive=True
        )
        
        for match in matches:
            stats['total_images'] += 1
            alt_text, image_url = match.groups()
            image_url = unquote(image_url)
            
            # 验证URL
            is_valid, url_type = is_valid_image_url(image_url)
            if not is_valid:
                logger.warning(f"跳过无效的URL: {image_url}")
                stats['failed_images'] += 1
                continue
                
            try:
                if url_type == 'svg':
                    # 处理SVG内容或URL
                    if is_svg_content(image_url):
                        # 保存内联SVG内容
                        svg_path = save_svg_content(image_url, temp_dir)
                        s3_key = f"images/{os.path.basename(svg_path)}"
                    else:
                        # 直接使用SVG URL
                        logger.info(f"保留SVG URL: {image_url}")
                        stats['svg_images'] += 1
                        continue
                        
                    # 检查是否是占位SVG
                    with open(svg_path, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                    if is_placeholder_svg(svg_content):
                        logger.info(f"跳过占位SVG: {image_url}")
                        stats['skipped_placeholders'] += 1
                        continue
                        
                    # 上传SVG文件
                    with open(svg_path, 'rb') as f:
                        await s3_client.upload_fileobj(
                            f,
                            bucket_name,
                            s3_key,
                            ExtraArgs={'ContentType': 'image/svg+xml'}
                        )
                        
                    # 创建新的URL
                    new_url = f"{public_url}/{s3_key}"
                    replacements.append((match.group(), f"![{alt_text}]({new_url})"))
                    stats['svg_images'] += 1
                    
                else:
                    # 处理普通图片
                    result = await image_processor.process_image(image_url, config)
                    
                    if result.success:
                        # 上传到S3
                        s3_key = f"images/{os.path.basename(result.output_path)}"
                        await upload_to_s3(result.output_path, s3_client, bucket_name, s3_key)
                        
                        # 创建新的URL
                        new_url = f"{public_url}/{s3_key}"
                        replacements.append((match.group(), f"![{alt_text}]({new_url})"))
                        
                        # 更新统计信息
                        stats['processed_images'] += 1
                        stats['total_size_before'] += result.stats.get('original_size', 0)
                        stats['total_size_after'] += result.stats.get('processed_size', 0)
                        
                        # 记录处理历史
                        history = ProcessingHistory(
                            original_url=image_url,
                            processed_url=new_url,
                            original_size=result.stats.get('original_size', 0),
                            processed_size=result.stats.get('processed_size', 0),
                            processing_time=result.stats.get('processing_time', 0)
                        )
                        session.add(history)
                        
                    else:
                        logger.error(f"处理图片失败: {image_url} - {result.error}")
                        stats['failed_images'] += 1
                        
            except Exception as e:
                logger.exception(f"处理图片时出错: {image_url}")
                stats['failed_images'] += 1
                
        # 应用替换
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
            
        # 保存修改后的文件
        output_path = os.path.join(temp_dir, f"processed_{os.path.basename(file_path)}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        await session.commit()
        
        return {
            'output_path': output_path,
            'stats': stats
        }
        
    except Exception as e:
        logger.exception("处理Markdown文件时出错")
        raise ProcessingError(f"处理Markdown文件失败: {str(e)}")

async def upload_to_s3(file_path: str, s3_client, bucket: str, key: str) -> str:
    """上传文件到S3

    Args:
        file_path: 本地文件路径
        s3_client: S3客户端
        bucket: 存储桶名称
        key: S3对象键

    Returns:
        str: S3 URL
    """
    try:
        with open(file_path, 'rb') as f:
            await s3_client.upload_fileobj(
                f,
                bucket,
                key,
                ExtraArgs={'ContentType': 'image/jpeg'}  # 假设是JPEG
            )
        return f"s3://{bucket}/{key}"
    except Exception as e:
        logger.exception(f"上传到S3失败: {file_path}")
        raise ProcessingError(f"上传到S3失败: {str(e)}")
