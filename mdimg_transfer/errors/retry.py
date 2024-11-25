"""重试策略实现"""

import asyncio
import logging
import random
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Type, Union, TypeVar, Any
from functools import wraps

from ..monitoring import MetricsCollector
from .exceptions import RetryableError

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2
    jitter: float = 0.1
    
    def get_delay(self, attempt: int) -> float:
        """计算下一次重试的延迟时间"""
        delay = min(
            self.base_delay * (self.exponential_base ** (attempt - 1)),
            self.max_delay
        )
        # 添加随机抖动
        jitter_range = delay * self.jitter
        return delay + random.uniform(-jitter_range, jitter_range)

def with_retry(
    error_types: Tuple[Type[Exception], ...] = (RetryableError,),
    config: Optional[RetryConfig] = None,
    metric_type: Optional[str] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """重试装饰器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            retry_config = config or RetryConfig()
            attempt = 0
            last_exception = None
            
            while attempt < retry_config.max_attempts:
                attempt += 1
                try:
                    start_time = time.time()
                    result = await func(*args, **kwargs)
                    if metric_type:
                        MetricsCollector.record_latency(metric_type, time.time() - start_time)
                    return result
                except error_types as e:
                    last_exception = e
                    if attempt < retry_config.max_attempts:
                        delay = retry_config.get_delay(attempt)
                        logger.warning(
                            f"Retry attempt {attempt}/{retry_config.max_attempts} "
                            f"for {func.__name__} after {delay:.2f}s: {str(e)}"
                        )
                        if metric_type:
                            MetricsCollector.record_retry(metric_type)
                        await asyncio.sleep(delay)
                    else:
                        if metric_type:
                            MetricsCollector.record_failure(metric_type)
                        raise
                except Exception as e:
                    if metric_type:
                        MetricsCollector.record_failure(metric_type)
                    raise

            raise last_exception

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            retry_config = config or RetryConfig()
            attempt = 0
            last_exception = None
            
            while attempt < retry_config.max_attempts:
                attempt += 1
                try:
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    if metric_type:
                        MetricsCollector.record_latency(metric_type, time.time() - start_time)
                    return result
                except error_types as e:
                    last_exception = e
                    if attempt < retry_config.max_attempts:
                        delay = retry_config.get_delay(attempt)
                        logger.warning(
                            f"Retry attempt {attempt}/{retry_config.max_attempts} "
                            f"for {func.__name__} after {delay:.2f}s: {str(e)}"
                        )
                        if metric_type:
                            MetricsCollector.record_retry(metric_type)
                        time.sleep(delay)
                    else:
                        if metric_type:
                            MetricsCollector.record_failure(metric_type)
                        raise
                except Exception as e:
                    if metric_type:
                        MetricsCollector.record_failure(metric_type)
                    raise

            raise last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator

class RetryContext:
    """重试上下文管理器"""
    def __init__(
        self,
        operation: str,
        config: Optional[RetryConfig] = None,
        error_types: Tuple[Type[Exception], ...] = (RetryableError,)
    ):
        self.operation = operation
        self.config = config or RetryConfig()
        self.error_types = error_types
        self.attempt = 0
        self.start_time = None

    async def __aenter__(self):
        self.attempt += 1
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False

        if not issubclass(exc_type, self.error_types):
            return False

        if self.attempt >= self.config.max_attempts:
            return False

        delay = self.config.get_delay(self.attempt)
        logger.warning(
            f"Retry attempt {self.attempt}/{self.config.max_attempts} "
            f"for {self.operation} after {delay:.2f}s: {str(exc_val)}"
        )
        await asyncio.sleep(delay)
        return True

async def retry_operation(
    operation: Callable[..., T],
    *args: Any,
    config: Optional[RetryConfig] = None,
    error_types: Tuple[Type[Exception], ...] = (RetryableError,),
    metric_type: Optional[str] = None,
    **kwargs: Any
) -> T:
    """重试操作的辅助函数"""
    retry_config = config or RetryConfig()
    attempt = 0
    last_exception = None
    
    while attempt < retry_config.max_attempts:
        attempt += 1
        try:
            start_time = time.time()
            result = await operation(*args, **kwargs)
            if metric_type:
                MetricsCollector.record_latency(metric_type, time.time() - start_time)
            return result
        except error_types as e:
            last_exception = e
            if attempt < retry_config.max_attempts:
                delay = retry_config.get_delay(attempt)
                logger.warning(
                    f"Retry attempt {attempt}/{retry_config.max_attempts} "
                    f"for operation after {delay:.2f}s: {str(e)}"
                )
                if metric_type:
                    MetricsCollector.record_retry(metric_type)
                await asyncio.sleep(delay)
            else:
                if metric_type:
                    MetricsCollector.record_failure(metric_type)
                raise
        except Exception as e:
            if metric_type:
                MetricsCollector.record_failure(metric_type)
            raise

    raise last_exception
