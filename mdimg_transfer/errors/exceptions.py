"""
异常类定义
"""

from typing import Optional

class BaseError(Exception):
    """基础错误类"""
    def __init__(self, message: str, error_type: str = "unknown", operation: str = "", details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.operation = operation
        self.details = details or {}

class ImageProcessingError(BaseError):
    """图片处理错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "image_processing_error", operation, details)

class StorageError(BaseError):
    """存储错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "storage_error", operation, details)

class NetworkError(BaseError):
    """网络错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "network_error", operation, details)

class ValidationError(BaseError):
    """验证错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "validation_error", operation, details)

class ConfigurationError(BaseError):
    """配置错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "configuration_error", operation, details)

class ResourceExhaustedError(BaseError):
    """资源耗尽错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "resource_exhausted", operation, details)

class QueueError(BaseError):
    """队列错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "queue_error", operation, details)

class RetryableError(BaseError):
    """可重试的错误"""
    def __init__(self, message: str, operation: str = "", details: Optional[dict] = None):
        super().__init__(message, "retryable_error", operation, details)
