"""监控装饰器"""

import time
import functools
from typing import Callable, Optional, Type, TypeVar
from .metrics import REQUEST_LATENCY, REQUEST_COUNT, PROCESSING_ERRORS

T = TypeVar('T')

def monitor_time(
    name: str,
    labels: Optional[dict] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    监控函数执行时间的装饰器

    Args:
        name: 指标名称
        labels: 标签

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            labels = labels or {}
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    status='success',
                    **labels
                ).inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(
                    status='error',
                    **labels
                ).inc()
                PROCESSING_ERRORS.labels(
                    type=type(e).__name__
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(**labels).observe(duration)
        return wrapper
    return decorator

def handle_exceptions(
    error_type: Type[Exception]
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    异常处理装饰器

    Args:
        error_type: 异常类型

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                PROCESSING_ERRORS.labels(
                    type=type(e).__name__
                ).inc()
                if isinstance(e, error_type):
                    raise
                raise error_type(str(e)) from e
        return wrapper
    return decorator
