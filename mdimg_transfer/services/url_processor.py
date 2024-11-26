"""
URL处理服务。
提供网页抓取和Markdown内容提取功能。
"""

import re
import logging
import aiohttp
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, Optional, List
from .file_processor import FileProcessor
from ..config import Config

logger = logging.getLogger(__name__)

class UrlProcessor:
    """URL处理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.file_processor = FileProcessor(config)
        
    async def _fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """获取URL内容"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.error(f"Error fetching URL {url}: HTTP {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None
            
    def _extract_markdown_content(self, html_content: str, base_url: str) -> str:
        """从HTML中提取Markdown内容"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除不需要的标签
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # 提取主要内容
            main_content = soup.find('article') or soup.find('main') or soup.find('body')
            if not main_content:
                return ''
            
            # 处理图片链接
            for img in main_content.find_all('img'):
                src = img.get('src', '')
                if src:
                    # 转换为绝对URL
                    abs_url = urljoin(base_url, src)
                    alt = img.get('alt', '')
                    img.replace_with(f'![{alt}]({abs_url})')
            
            # 处理其他标签
            content = main_content.get_text('\n', strip=True)
            
            # 清理多余的空行
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            return content
            
        except Exception as e:
            logger.error(f"Error extracting markdown content: {e}")
            return ''
            
    async def process_url(self, url: str, task_id: str, progress_callback=None) -> Dict[str, Any]:
        """处理URL并返回结果"""
        try:
            # 验证URL
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return {'error': '无效的URL'}
            
            # 获取页面内容
            if progress_callback:
                progress_callback({
                    'message': '正在获取页面内容...',
                    'progress': 0
                })
                
            html_content = await self._fetch_url(url)
            if not html_content:
                return {'error': '无法获取页面内容'}
            
            # 提取Markdown内容
            if progress_callback:
                progress_callback({
                    'message': '正在提取内容...',
                    'progress': 30
                })
                
            markdown_content = self._extract_markdown_content(html_content, url)
            if not markdown_content:
                return {'error': '无法提取有效内容'}
            
            # 创建临时Markdown文件
            filename = f"{urlparse(url).netloc.replace('.', '_')}.md"
            temp_file_path = Path(self.config.temp_dir) / filename
            
            # 确保临时目录存在
            temp_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with temp_file_path.open('w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # 处理文件中的图片
            if progress_callback:
                progress_callback({
                    'message': '正在处理图片...',
                    'progress': 60
                })
            
            # 使用文件处理器处理图片
            from werkzeug.datastructures import FileStorage
            with temp_file_path.open('rb') as f:
                file = FileStorage(f, filename=filename)
                result = await self.file_processor.process_markdown_file(
                    file=file,
                    task_id=task_id,
                    progress_callback=lambda p: progress_callback({
                        'message': p['message'],
                        'progress': 60 + int(p['progress'] * 0.4),
                        'details': p['details']
                    }) if progress_callback else None
                )
            
            # 清理临时文件
            temp_file_path.unlink()
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            return {'error': str(e)}
