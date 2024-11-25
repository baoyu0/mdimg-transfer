"""错误处理函数"""

import logging
import asyncio
from typing import Optional, Type, TypeVar, Callable, Any
from functools import wraps
from .exceptions import (
    BaseError,
    ImageProcessingError,
    StorageError,
    ValidationError,
)
from ..monitoring import ProcessingMetrics

logger = logging.getLogger(__name__)

T = TypeVar('T')

def handle_processing_error(func: Callable[..., T]) -> Callable[..., T]:
    """处理图片处理错误的装饰器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except ImageProcessingError as e:
            logger.error(f"Image processing error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            ProcessingMetrics.record_error(e.error_type)
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in image processing: {str(e)}")
            ProcessingMetrics.record_error('unexpected')
            raise ImageProcessingError(str(e), func.__name__, {'original_error': str(e)})

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except ImageProcessingError as e:
            logger.error(f"Image processing error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            ProcessingMetrics.record_error(e.error_type)
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in image processing: {str(e)}")
            ProcessingMetrics.record_error('unexpected')
            raise ImageProcessingError(str(e), func.__name__, {'original_error': str(e)})

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

def handle_storage_error(func: Callable[..., T]) -> Callable[..., T]:
    """处理存储错误的装饰器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except StorageError as e:
            logger.error(f"Storage error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            raise
        except Exception as e:
            logger.exception(f"Unexpected storage error: {str(e)}")
            raise StorageError(str(e), func.__name__, {'original_error': str(e)})

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except StorageError as e:
            logger.error(f"Storage error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            raise
        except Exception as e:
            logger.exception(f"Unexpected storage error: {str(e)}")
            raise StorageError(str(e), func.__name__, {'original_error': str(e)})

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

def handle_validation_error(func: Callable[..., T]) -> Callable[..., T]:
    """处理验证错误的装饰器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            raise
        except Exception as e:
            logger.exception(f"Unexpected validation error: {str(e)}")
            raise ValidationError(str(e), func.__name__, {'original_error': str(e)})

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in {e.operation}: {str(e)}", 
                        extra={'error_type': e.error_type, 'details': e.details})
            raise
        except Exception as e:
            logger.exception(f"Unexpected validation error: {str(e)}")
            raise ValidationError(str(e), func.__name__, {'original_error': str(e)})

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
