"""统一的错误处理模块"""

from .exceptions import (
    ImageProcessingError,
    StorageError,
    ValidationError,
    NetworkError,
    ResourceExhaustedError,
    ConfigurationError,
    QueueError,
    BaseError
)
from .retry import RetryConfig, with_retry, RetryContext
from .handlers import (
    handle_processing_error,
    handle_storage_error,
    handle_validation_error,
)

__all__ = [
    'ImageProcessingError',
    'StorageError',
    'ValidationError',
    'NetworkError',
    'ResourceExhaustedError',
    'ConfigurationError',
    'QueueError',
    'BaseError',
    'RetryConfig',
    'with_retry',
    'RetryContext',
    'handle_processing_error',
    'handle_storage_error',
    'handle_validation_error',
]
