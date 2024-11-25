"""
Markdown处理器模块
"""
import re
import os
import aiohttp
import logging
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from urllib.parse import urlparse, unquote
from .image_downloader import ImageDownloader
from .r2_uploader import R2Uploader
from ..config import config

@dataclass
class ImageLink:
    """图片链接数据类"""
    alt: str
    url: str
    title: str = ""

class MarkdownProcessor:
    """Markdown处理器类"""
    
    # 图片链接正则表达式
    IMAGE_PATTERN = r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)'
    
    def __init__(self, downloader: ImageDownloader, r2_uploader: R2Uploader):
        """初始化 Markdown 处理器
        
        Args:
            downloader: 图片下载器实例
            r2_uploader: R2上传器实例
        """
        self.downloader = downloader
        self._r2_uploader = r2_uploader
        self.image_links = []
        self.logger = logging.getLogger('mdimg_transfer.markdown_processor')
        self.errors = []  # Add error tracking list

    @property
    def r2_uploader(self):
        """延迟初始化R2上传器"""
        if self._r2_uploader is None:
            self._r2_uploader = R2Uploader()
        return self._r2_uploader
        
    def parse_image_links(self, content: str) -> List[ImageLink]:
        """
        解析 Markdown 文件内容，提取所有图片链接。
        支持标准 Markdown 和扩展语法。
        
        Args:
            content: Markdown 文本内容
            
        Returns:
            List[ImageLink]: 图片链接列表
        """
        # 标准 Markdown 图片语法
        standard_pattern = r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)'
        
        # HTML 图片标签语法
        html_pattern = r'<img.*?src=["\'](.*?)["\'].*?alt=["\'](.*?)["\'].*?>'
        
        # 收集所有匹配的图片链接
        image_links = []
        
        # 处理标准 Markdown 语法
        for match in re.finditer(standard_pattern, content):
            alt = match.group(1)
            url = unquote(match.group(2))
            title = match.group(3) or ""
            
            # 验证URL
            if self._is_valid_url(url):
                image_links.append(ImageLink(alt=alt, url=url, title=title))
            else:
                self.logger.warning(f"跳过无效的图片URL: {url}")
        
        # 处理 HTML 图片标签
        for match in re.finditer(html_pattern, content):
            url = unquote(match.group(1))
            alt = match.group(2)
            
            # 验证URL
            if self._is_valid_url(url):
                image_links.append(ImageLink(alt=alt, url=url))
            else:
                self.logger.warning(f"跳过无效的图片URL: {url}")
        
        self.image_links = image_links
        self.logger.info("找到 %d 个图片链接", len(self.image_links))
        return image_links
        
    def _is_valid_url(self, url: str) -> bool:
        """验证URL是否有效"""
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
            
    async def process_content(self, content: str) -> Tuple[str, Dict[str, Tuple[bool, str]]]:
        """处理 Markdown 内容。

        Args:
            content: Markdown 内容

        Returns:
            处理后的内容和下载结果的元组
        """
        self.logger.info("开始处理Markdown文本，长度: %d", len(content))
        
        self.content = content
        self.image_links = self.parse_image_links(content)
        
        if not self.image_links:
            self.logger.info("未找到任何图片链接")
            return content, {}
            
        download_results = {}
        new_content = content
        
        try:
            # 批量下载图片
            urls = [link.url for link in self.image_links]
            download_results_dict = await self.downloader.download_images(urls)
            
            # 处理每个链接
            for link in self.image_links:
                local_path = download_results_dict.get(link.url)
                if not local_path:
                    self.logger.error("下载图片失败: %s", link.url)
                    download_results[link.url] = (False, "下载失败")
                    continue
                    
                # 上传到 R2
                try:
                    filename = os.path.basename(local_path)
                    r2_url = await self.r2_uploader.upload_image(local_path, filename)
                    self.logger.info("成功上传图片到R2: %s -> %s", local_path, r2_url)
                    
                    # 替换链接
                    if '"' in link.title:
                        old_link = f'![{link.alt}]({link.url} "{link.title}")'
                    else:
                        old_link = f'![{link.alt}]({link.url})'
                        
                    if '"' in link.title:
                        new_link = f'![{link.alt}]({r2_url} "{link.title}")'
                    else:
                        new_link = f'![{link.alt}]({r2_url})'
                        
                    new_content = new_content.replace(old_link, new_link)
                    self.logger.info("替换图片链接: %s -> %s", link.url, r2_url)
                    download_results[link.url] = (True, r2_url)
                    
                except Exception as e:
                    self.logger.error("上传到R2失败: %s", str(e))
                    download_results[link.url] = (False, f"上传失败: {str(e)}")
                    self.errors.append(str(e))  # Add error to tracking list
                    
        except Exception as e:
            self.logger.error("处理图片失败: %s", str(e))
            for link in self.image_links:
                download_results[link.url] = (False, str(e))
            self.errors.append(str(e))  # Add error to tracking list
                
        successful_downloads = sum(1 for result in download_results.values() if result[0])
        self.logger.info("处理完成！成功: %d, 失败: %d", successful_downloads, len(self.image_links) - successful_downloads)
        
        return new_content, download_results
