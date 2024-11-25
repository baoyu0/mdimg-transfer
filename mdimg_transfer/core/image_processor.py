"""
图片处理核心模块。
提供图片下载、上传和处理功能。
"""

import os
import io
import logging
import hashlib
import mimetypes
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
from PIL import Image, ImageOps
import asyncio
import aiohttp
import aiofiles
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from ..monitoring import MetricsCollector
from ..errors import (
    ImageProcessingError,
    handle_processing_error,
    RetryConfig,
    with_retry
)
from .config import ImageConfig

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """图片处理结果"""
    success: bool
    output_path: Optional[str]
    mime_type: Optional[str]
    stats: Dict[str, Any]
    error: Optional[str] = None

class ImageProcessor:
    """统一的图片处理器"""
    
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'}
    
    def __init__(
            self,
            executor: Optional[ThreadPoolExecutor] = None,
            cache_dir: Optional[str] = None,
            retry_config: Optional[RetryConfig] = None,
            max_retries: int = 3,
            timeout: int = 30,
            max_concurrent_downloads: int = 5,
            temp_dir: str = "temp",
            config: Optional[ImageConfig] = None
        ):
        """
        初始化图片处理器
        
        Args:
            executor: 线程池执行器
            cache_dir: 缓存目录
            retry_config: 重试配置
            max_retries: 最大重试次数
            timeout: 超时时间(秒)
            max_concurrent_downloads: 最大并发下载数
            temp_dir: 临时文件目录
            config: 图片处理配置
        """
        self.executor = executor or ThreadPoolExecutor(max_workers=3)
        self.cache_dir = cache_dir
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.retry_config = retry_config or RetryConfig()
        self.metrics = MetricsCollector()
        
        # 下载相关配置
        self.max_retries = max_retries
        self.timeout = timeout
        self.max_concurrent_downloads = max_concurrent_downloads
        self.download_semaphore = asyncio.Semaphore(max_concurrent_downloads)
        self.session = None
        self.processing_state = {}  # 记录每个URL的处理状态
        self.failed_urls = set()    # 记录失败的URL
        
        # 设置临时目录
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        
        # 设置图片处理配置
        self.processing_config = config or ImageConfig()
        self.MAX_IMAGE_SIZE = self.processing_config.max_file_size

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
        self.executor.shutdown(wait=False)

    def _get_safe_filename(self, url: str) -> str:
        """生成安全的文件名"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path:
            # 如果URL没有路径，使用URL的哈希作为文件名
            return hashlib.md5(url.encode()).hexdigest()
        
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        if not ext:
            # 如果没有扩展名，尝试从Content-Type推断
            ext = mimetypes.guess_extension(self.session.headers.get('content-type', '')) or '.bin'
        
        # 移除不安全字符
        safe_name = ''.join(c for c in name if c.isalnum() or c in '-_')
        return f"{safe_name}{ext}"

    @with_retry()
    async def download_image(self, url: str) -> Tuple[str, str]:
        """
        下载图片
        
        Args:
            url: 图片URL
            
        Returns:
            Tuple[str, str]: (临时文件路径, MIME类型)
        """
        async with self.download_semaphore:
            try:
                async with self.session.get(url) as response:
                    if response.status != 200:
                        raise ImageProcessingError(f"下载失败: HTTP {response.status}")
                    
                    content_type = response.headers.get('content-type', '')
                    if not content_type.startswith('image/'):
                        raise ImageProcessingError(f"不是图片: {content_type}")
                    
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > self.MAX_IMAGE_SIZE:
                        raise ImageProcessingError(f"图片太大: {content_length} bytes")
                    
                    temp_path = os.path.join(self.temp_dir, self._get_safe_filename(url))
                    async with aiofiles.open(temp_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    
                    return temp_path, content_type
                    
            except asyncio.TimeoutError:
                raise ImageProcessingError("下载超时")
            except aiohttp.ClientError as e:
                raise ImageProcessingError(f"下载错误: {str(e)}")
            except Exception as e:
                raise ImageProcessingError(f"下载错误: {str(e)}")

    async def process_image(
            self,
            input_path: str,
            config: Optional[Dict] = None
        ) -> ProcessingResult:
        """
        处理图片
        
        Args:
            input_path: 输入图片路径
            config: 处理配置，覆盖默认配置
                - quality: 压缩质量 (1-100)
                - max_width: 最大宽度
                - max_height: 最大高度
                - format: 目标格式
                - strip_metadata: 是否清除元数据
                
        Returns:
            ProcessingResult: 处理结果
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._process_image_sync,
                input_path,
                config or {}
            )
            return result
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                mime_type=None,
                stats={},
                error=str(e)
            )

    def _process_image_sync(
            self,
            input_path: str,
            config: Dict
        ) -> ProcessingResult:
        """同步处理图片"""
        try:
            with Image.open(input_path) as img:
                # 基本信息
                format = img.format
                mime_type = Image.MIME[format]
                
                # 检查MIME类型
                if mime_type not in self.ALLOWED_MIME_TYPES:
                    raise ImageProcessingError(f"不支持的图片格式: {mime_type}")
                
                # 处理选项
                quality = config.get('quality', self.processing_config.quality)
                max_width = config.get('max_width', self.processing_config.max_width)
                max_height = config.get('max_height', self.processing_config.max_height)
                strip_metadata = config.get('strip_metadata', self.processing_config.strip_metadata)
                target_format = config.get('format', self.processing_config.format)
                if target_format == 'auto':
                    target_format = format
                
                # 调整大小
                if max_width or max_height:
                    img.thumbnail((max_width, max_height), Image.LANCZOS)
                
                # 清除元数据
                if strip_metadata:
                    img = ImageOps.exif_transpose(img)
                    
                # 优化大小
                output = io.BytesIO()
                save_args = {'format': target_format}
                
                if target_format in ('JPEG', 'WEBP'):
                    save_args['quality'] = quality
                    if target_format == 'JPEG':
                        save_args['progressive'] = True
                        save_args['optimize'] = True
                elif target_format == 'PNG':
                    save_args['optimize'] = True
                
                img.save(output, **save_args)
                
                # 检查输出大小
                output_size = output.tell()
                if output_size > self.MAX_IMAGE_SIZE:
                    if target_format in ('JPEG', 'WEBP'):
                        # 尝试通过降低质量来减小文件大小
                        output, quality = self._optimize_image_size(
                            img, target_format, quality, self.MAX_IMAGE_SIZE
                        )
                    else:
                        raise ImageProcessingError(f"处理后的图片太大: {output_size} bytes")
                
                # 保存结果
                output_path = os.path.join(
                    self.cache_dir,
                    f"{os.path.splitext(os.path.basename(input_path))[0]}_processed.{target_format.lower()}"
                )
                with open(output_path, 'wb') as f:
                    f.write(output.getvalue())
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    mime_type=Image.MIME[target_format],
                    stats={
                        'original_size': os.path.getsize(input_path),
                        'processed_size': output_size,
                        'width': img.width,
                        'height': img.height,
                        'format': target_format,
                        'quality': quality
                    }
                )
                
        except Exception as e:
            error_msg = handle_processing_error(e)
            logger.error(f"图片处理错误: {error_msg}")
            return ProcessingResult(
                success=False,
                output_path=None,
                mime_type=None,
                stats={},
                error=error_msg
            )

    def _optimize_image_size(
            self,
            image: Image.Image,
            format: str,
            initial_quality: int,
            max_size: int
        ) -> Tuple[io.BytesIO, int]:
        """
        优化图片大小
        
        Args:
            image: PIL图片对象
            format: 目标格式
            initial_quality: 初始质量
            max_size: 最大文件大小
            
        Returns:
            Tuple[io.BytesIO, int]: (优化后的图片数据, 最终质量)
        """
        quality = initial_quality
        output = io.BytesIO()
        
        while quality > 5:  # 最低质量限制
            output = io.BytesIO()
            save_args = {
                'format': format,
                'quality': quality
            }
            if format == 'JPEG':
                save_args.update({
                    'progressive': True,
                    'optimize': True
                })
            
            image.save(output, **save_args)
            if output.tell() <= max_size:
                break
                
            quality -= 5
        
        return output, quality

    def get_mime_type(self, file_path: str) -> str:
        """
        获取文件的 MIME 类型。
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: MIME 类型
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'

    async def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {e}")
        except Exception as e:
            logger.error(f"清理临时目录失败: {e}")
