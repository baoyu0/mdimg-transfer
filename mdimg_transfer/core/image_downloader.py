"""
图片下载和处理模块
"""
import os
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from urllib.parse import urlparse, unquote
import logging
import time
from ..config import config
from PIL import Image
import io
from bs4 import BeautifulSoup

class ImageDownloader:
    """图片下载器，用于下载远程图片到本地临时目录"""
    
    def __init__(self):
        """初始化图片下载器"""
        self.session: Optional[aiohttp.ClientSession] = None
        self.download_semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_DOWNLOADS)
        self.max_retries = config.MAX_RETRIES
        self.download_timeout = config.DOWNLOAD_TIMEOUT
        self.max_file_size = config.MAX_FILE_SIZE
        self.temp_dir = config.TEMP_DIR
        self.processing_state: Dict[str, Dict[str, any]] = {}
        self.failed_urls: set[str] = set()
        self.logger = logging.getLogger('mdimg_transfer.image_downloader')
        self.logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别以记录详细信息
        
    async def __aenter__(self):
        """创建HTTP会话"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://mp.weixin.qq.com/'
            })
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None
            
    def _get_safe_filename(self, url: str) -> str:
        """从URL中提取文件名"""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)
        
        # 如果URL没有文件名，使用URL的hash作为文件名
        if not filename or '.' not in filename:
            filename = f"image_{hash(url)}.jpg"
            
        return filename
        
    async def _get_wechat_cookies(self) -> dict:
        """获取微信文章页面的cookies"""
        self.logger.info("尝试获取微信cookies...")
        try:
            article_url = "https://mp.weixin.qq.com/s/qNbkGCrvZM1WO6FXf9M4kQ"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            self.logger.debug(f"访问文章页面: {article_url}")
            self.logger.debug(f"使用请求头: {headers}")
            
            async with self.session.get(
                article_url,
                headers=headers,
                verify_ssl=False,
                allow_redirects=True,
                timeout=30
            ) as response:
                self.logger.debug(f"文章页面响应状态码: {response.status}")
                self.logger.debug(f"响应头: {response.headers}")
                
                if response.status == 200:
                    cookies = response.cookies
                    cookie_dict = {cookie.key: cookie.value for cookie in cookies.values()}
                    self.logger.debug(f"获取到cookies: {cookie_dict}")
                    return cookie_dict
                else:
                    self.logger.warning(f"无法获取cookies，状态码: {response.status}")
                    return {}
                    
        except Exception as e:
            self.logger.error(f"获取cookies失败: {str(e)}", exc_info=True)
            return {}
            
    def _get_headers_for_url(self, url: str) -> dict:
        """根据URL获取合适的请求头"""
        is_wechat = 'mmbiz.qpic.cn' in url
        is_gif = 'wx_fmt=gif' in url or '.gif' in url.lower()
        
        # 基础请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Site': 'cross-site'
        }
        
        if is_wechat:
            # 微信特定请求头
            headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309071d)' if is_gif else headers['User-Agent'],
                'Referer': 'https://mp.weixin.qq.com/',
                'Origin': 'https://mp.weixin.qq.com',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            })
            
        return headers
        
    def _process_wechat_url(self, url: str) -> str:
        """处理微信图片URL，保留所有原始参数"""
        # 如果URL中没有参数，添加基本参数
        if '?' not in url:
            return f"{url}?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1"
            
        # 解析现有参数
        base_url, query = url.split('?', 1)
        params = {}
        for param in query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
                
        # 确保必要的参数存在
        if 'wx_fmt' not in params and 'tp' not in params:
            # 从URL路径尝试检测格式
            if '.gif' in base_url.lower():
                params['wx_fmt'] = 'gif'
            else:
                params['wx_fmt'] = 'png'
        if 'wxfrom' not in params:
            params['wxfrom'] = '5'
        if 'wx_lazy' not in params:
            params['wx_lazy'] = '1'
        if 'wx_co' not in params:
            params['wx_co'] = '1'
            
        # 重建URL
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{query_string}"
        
    async def _download_single_image(self, url: str) -> Optional[str]:
        """下载单个图片"""
        self.logger.info(f"开始下载图片: {url}")
        
        if not url:
            self.logger.error("URL为空")
            return None
            
        if url in self.failed_urls:
            self.logger.warning(f"跳过之前失败的URL: {url}")
            return None
            
        self.processing_state[url] = {
            'status': 'downloading',
            'retries': 0,
            'start_time': time.time(),
            'errors': []
        }
        
        try:
            async with self.download_semaphore:
                # 处理微信图片URL
                is_wechat = 'mmbiz.qpic.cn' in url
                is_gif = 'wx_fmt=gif' in url or '.gif' in url.lower()
                
                if is_wechat:
                    original_url = url
                    url = self._process_wechat_url(url)
                    self.logger.debug(f"处理后的微信图片URL: {url}")
                    if is_gif:
                        self.logger.debug("检测到GIF图片，获取微信cookies")
                        cookies = await self._get_wechat_cookies()
                        if not cookies:
                            self.logger.warning("未能获取微信cookies，尝试使用备用参数")
                            # 尝试不同的参数组合
                            url = original_url.replace('&tp=webp', '').replace('&wxfrom=5', '').replace('&wx_lazy=1', '')
                            if '?' in url:
                                url += '&wx_co=1'
                            else:
                                url += '?wx_co=1'
                    else:
                        cookies = None
                else:
                    self.logger.debug("非微信图片，跳过获取cookies")
                    cookies = None
                
                filename = self._get_safe_filename(url)
                if is_gif and not filename.lower().endswith('.gif'):
                    filename = filename.rsplit('.', 1)[0] + '.gif'
                    
                temp_path = os.path.join(self.temp_dir, f"temp_{filename}")
                self.logger.debug(f"临时文件路径: {temp_path}")
                
                headers = self._get_headers_for_url(url)
                self.logger.debug(f"使用请求头: {headers}")
                
                last_error = None
                for attempt in range(self.max_retries):
                    try:
                        self.logger.info(f"尝试下载 {url} (尝试 {attempt + 1}/{self.max_retries})")
                        
                        async with self.session.get(
                            url,
                            headers=headers,
                            cookies=cookies,
                            verify_ssl=False,
                            timeout=self.download_timeout * (attempt + 1),  # 随重试次数增加超时时间
                            allow_redirects=True
                        ) as response:
                            self.logger.debug(f"响应状态码: {response.status}")
                            self.logger.debug(f"响应头: {response.headers}")
                            
                            if response.status == 200:
                                content_type = response.headers.get('Content-Type', '')
                                self.logger.debug(f"Content-Type: {content_type}")
                                
                                # 更新内容类型检查，添加 SVG 支持
                                valid_types = [
                                    'image/', 
                                    'webp', 
                                    'application/octet-stream', 
                                    'binary/octet-stream',
                                    'image/svg+xml',  # 添加 SVG 支持
                                    'application/xml',  # 某些服务器可能使用这个 MIME 类型
                                    'text/xml'  # 某些服务器可能使用这个 MIME 类型
                                ]
                                
                                if not any(ct in content_type.lower() for ct in valid_types):
                                    error_msg = f"响应不是图片: {content_type}"
                                    self.logger.error(error_msg)
                                    raise ValueError(error_msg)
                                
                                content_length = response.headers.get('Content-Length')
                                if content_length:
                                    size = int(content_length)
                                    self.logger.debug(f"Content-Length: {size:,} bytes")
                                    if size > self.max_file_size:
                                        error_msg = f"文件太大: {size:,} bytes (最大限制: {self.max_file_size:,} bytes)"
                                        self.logger.error(error_msg)
                                        raise ValueError(error_msg)
                                
                                content = await response.read()
                                actual_size = len(content)
                                self.logger.debug(f"下载内容大小: {actual_size:,} bytes")
                                
                                if content_length and actual_size != int(content_length):
                                    error_msg = f"下载内容大小不匹配: 期望 {content_length} bytes, 实际 {actual_size} bytes"
                                    self.logger.error(error_msg)
                                    raise ValueError(error_msg)
                                
                                # 使用BytesIO验证图片
                                try:
                                    # 检查是否是 SVG
                                    if any(ct in content_type.lower() for ct in ['svg', 'xml']):
                                        # SVG 格式验证
                                        svg_content = content.decode('utf-8')
                                        if not ('<svg' in svg_content and '</svg>' in svg_content):
                                            raise ValueError("无效的 SVG 文件")
                                        self.logger.info("SVG 验证成功")
                                    else:
                                        # 其他图片格式验证
                                        with Image.open(io.BytesIO(content)) as img:
                                            # 对于GIF，验证帧数
                                            if img.format == 'GIF':
                                                try:
                                                    frames = 0
                                                    while True:
                                                        frames += 1
                                                        img.seek(img.tell() + 1)
                                                except EOFError:
                                                    pass
                                                self.logger.info(f"GIF验证成功: 格式={img.format}, 大小={img.size}, 帧数={frames}")
                                            else:
                                                img.verify()
                                                self.logger.info(f"图片验证成功: 格式={img.format}, 大小={img.size}")
                                        
                                    # 验证成功后再保存文件
                                    async with aiofiles.open(temp_path, 'wb') as f:
                                        await f.write(content)
                                        
                                    return temp_path
                                    
                                except Exception as e:
                                    error_msg = f"图片验证失败: {str(e)}"
                                    self.logger.error(error_msg)
                                    last_error = e
                                    if attempt == self.max_retries - 1:
                                        raise ValueError(error_msg)
                                    continue
                                    
                            else:
                                error_msg = f"下载失败: HTTP {response.status}"
                                self.logger.error(error_msg)
                                last_error = ValueError(error_msg)
                                if attempt == self.max_retries - 1:
                                    raise last_error
                                continue
                                
                    except asyncio.TimeoutError as e:
                        error_msg = f"下载超时 (尝试 {attempt + 1}/{self.max_retries})"
                        self.logger.warning(error_msg)
                        last_error = e
                        if attempt == self.max_retries - 1:
                            raise
                            
                    except Exception as e:
                        error_msg = f"下载出错: {str(e)} (尝试 {attempt + 1}/{self.max_retries})"
                        self.logger.error(error_msg)
                        last_error = e
                        if attempt == self.max_retries - 1:
                            raise
                            
                        await asyncio.sleep(1 * (attempt + 1))  # 指数退避
                        
        except Exception as e:
            self.logger.error(f"下载失败: {url}", exc_info=True)
            if last_error:
                self.logger.error(f"最后一次错误: {str(last_error)}")
            self.failed_urls.add(url)
            self.processing_state[url]['status'] = 'failed'
            self.processing_state[url]['errors'].append(str(e))
            return None
            
    async def download_url_content(self, url: str) -> str:
        """
        下载URL内容并转换为Markdown格式。
        
        Args:
            url: 要下载的URL
            
        Returns:
            str: 转换后的Markdown内容
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    
                    content_type = response.headers.get('content-type', '').lower()
                    if 'text/html' not in content_type:
                        return None
                    
                    html_content = await response.text()
                    
                    # 使用BeautifulSoup解析HTML
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # 移除不需要的标签
                    for tag in soup(['script', 'style']):
                        tag.decompose()
                    
                    # 提取标题
                    title = soup.title.string if soup.title else 'Untitled'
                    markdown_content = [f"# {title}\n"]
                    
                    # 处理正文内容
                    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a', 'ul', 'ol', 'li']):
                        if element.name == 'p':
                            text = element.get_text().strip()
                            if text:
                                markdown_content.append(f"{text}\n")
                        elif element.name.startswith('h'):
                            level = int(element.name[1])
                            text = element.get_text().strip()
                            if text:
                                markdown_content.append(f"{'#' * level} {text}\n")
                        elif element.name == 'img':
                            src = element.get('src', '')
                            alt = element.get('alt', '')
                            if src:
                                markdown_content.append(f"![{alt}]({src})\n")
                        elif element.name == 'a':
                            href = element.get('href', '')
                            text = element.get_text().strip()
                            if href and text:
                                markdown_content.append(f"[{text}]({href})\n")
                        elif element.name == 'ul':
                            for li in element.find_all('li', recursive=False):
                                text = li.get_text().strip()
                                if text:
                                    markdown_content.append(f"- {text}\n")
                        elif element.name == 'ol':
                            for i, li in enumerate(element.find_all('li', recursive=False), 1):
                                text = li.get_text().strip()
                                if text:
                                    markdown_content.append(f"{i}. {text}\n")
                    
                    return '\n'.join(markdown_content)
                    
        except Exception as e:
            self.logger.error(f"Error downloading URL content: {str(e)}")
            return None
            
    async def download_images(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """批量下载图片
        
        Args:
            urls: 图片URL列表
            
        Returns:
            Dict[str, Optional[str]]: 键为URL，值为下载后的文件路径或None（表示下载失败）
        """
        results = {}
        
        async with self:  # 确保session被正确创建和关闭
            tasks = []
            self.logger.info(f"开始批量下载 {len(urls)} 个图片")
            
            for url in urls:
                task = asyncio.create_task(
                    self._download_single_image(url)
                )
                tasks.append(task)
                
            # 等待所有任务完成
            self.logger.info("等待所有下载任务完成")
            completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理结果
            for url, result in zip(urls, completed_tasks):
                if isinstance(result, Exception):
                    self.logger.error(f"下载失败 {url}: {str(result)}")
                    results[url] = None
                else:
                    if result:
                        self.logger.info(f"下载成功: {url} -> {result}")
                    else:
                        self.logger.error(f"下载失败: {url}")
                    results[url] = result
            
            self.logger.info(f"批量下载完成，成功: {sum(1 for r in results.values() if r)}/{len(urls)}")
            return results
