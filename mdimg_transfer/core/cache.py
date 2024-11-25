"""缓存管理模块"""

import asyncio
import hashlib
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar

from .metrics import metrics

logger = logging.getLogger(__name__)
T = TypeVar('T')

class Cache:
    """LRU缓存实现"""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        初始化缓存

        Args:
            max_size: 最大缓存条目数
            ttl: 缓存过期时间(秒)
        """
        self._cache: Dict[str, Any] = {}
        self._access_times: Dict[str, datetime] = {}
        self._max_size = max_size
        self._ttl = ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值，不存在返回None
        """
        async with self._lock:
            if key not in self._cache:
                metrics.track_cache_operation("get", "miss")
                return None

            # 检查是否过期
            access_time = self._access_times[key]
            if datetime.now() - access_time > timedelta(seconds=self._ttl):
                await self._remove(key)
                metrics.track_cache_operation("get", "miss")
                return None

            # 更新访问时间
            self._access_times[key] = datetime.now()
            metrics.track_cache_operation("get", "success")
            return self._cache[key]

    async def set(self, key: str, value: Any) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
        """
        async with self._lock:
            # 检查容量
            if len(self._cache) >= self._max_size:
                # 移除最久未使用的项
                oldest_key = min(
                    self._access_times.items(),
                    key=lambda x: x[1]
                )[0]
                await self._remove(oldest_key)

            self._cache[key] = value
            self._access_times[key] = datetime.now()
            metrics.update_cache_size(len(self._cache))
            metrics.track_cache_operation("set", "success")

    async def _remove(self, key: str) -> None:
        """
        移除缓存项

        Args:
            key: 缓存键
        """
        del self._cache[key]
        del self._access_times[key]
        metrics.update_cache_size(len(self._cache))
        metrics.track_cache_operation("delete", "success")

    async def clear(self) -> None:
        """清空缓存"""
        async with self._lock:
            self._cache.clear()
            self._access_times.clear()
            metrics.update_cache_size(0)
            metrics.track_cache_operation("clear", "success")

def cache_key(*args, **kwargs) -> str:
    """生成缓存键

    Args:
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        缓存键字符串
    """
    key_parts = []
    
    # 添加位置参数
    for arg in args:
        key_parts.append(str(arg))
    
    # 添加关键字参数
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    # 生成MD5哈希
    key = hashlib.md5(":".join(key_parts).encode()).hexdigest()
    return key

def cached(cache_instance: Cache, ttl: Optional[int] = None):
    """
    缓存装饰器

    Args:
        cache_instance: 缓存实例
        ttl: 过期时间(秒)，None表示使用缓存默认值

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # 生成缓存键
            key = cache_key(func.__name__, *args, **kwargs)

            # 尝试从缓存获取
            cached_value = await cache_instance.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value

            # 执行函数
            logger.debug(f"Cache miss for {func.__name__}")
            result = await func(*args, **kwargs)

            # 存入缓存
            await cache_instance.set(key, result)
            return result

        return wrapper
    return decorator
