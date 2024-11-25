"""
错误处理模块
"""

import asyncio
import functools
import logging
import aiohttp
from dataclasses import dataclass
from typing import Optional, Callable, Any

logger = logging.getLogger(__name__)

class ImageProcessingError(Exception):
    """图片处理错误"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3
    delay: float = 1.0
    backoff_factor: float = 2.0
    exceptions: tuple = (ImageProcessingError,)

def with_retry(func: Optional[Callable] = None, *, config: Optional[RetryConfig] = None):
    """
    重试装饰器
    
    Args:
        func: 被装饰的函数
        config: 重试配置
    """
    if func is None:
        return functools.partial(with_retry, config=config)
        
    retry_config = config or RetryConfig()
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(retry_config.max_retries):
            try:
                return await func(*args, **kwargs)
            except retry_config.exceptions as e:
                last_exception = e
                if attempt < retry_config.max_retries - 1:
                    delay = retry_config.delay * (retry_config.backoff_factor ** attempt)
                    logger.warning(
                        f"重试 {func.__name__} (尝试 {attempt + 1}/{retry_config.max_retries}): {str(e)}"
                    )
                    await asyncio.sleep(delay)
        
        raise last_exception
        
    return wrapper

def handle_processing_error(error: Exception) -> str:
    """
    处理图片处理错误
    
    Args:
        error: 异常对象
        
    Returns:
        str: 错误消息
    """
    if isinstance(error, ImageProcessingError):
        return str(error)
    elif isinstance(error, (IOError, OSError)):
        return f"文件操作错误: {str(error)}"
    elif isinstance(error, ValueError):
        return f"值错误: {str(error)}"
    elif isinstance(error, aiohttp.ClientError):
        return f"HTTP客户端错误: {str(error)}"
    else:
        return f"未知错误: {str(error)}"
