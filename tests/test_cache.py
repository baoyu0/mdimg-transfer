"""缓存测试模块"""

import pytest
import asyncio
from mdimg_transfer.core.cache import Cache
from mdimg_transfer.monitoring.metrics import CACHE_OPERATIONS, CACHE_SIZE

@pytest.mark.asyncio
async def test_cache_basic_operations():
    """测试基本的缓存操作"""
    cache = Cache(max_size=2)
    
    # 测试设置和获取
    await cache.set("key1", b"value1")
    value = await cache.get("key1")
    assert value == b"value1"
    
    # 测试不存在的键
    value = await cache.get("nonexistent")
    assert value is None
    
    # 测试缓存容量限制
    await cache.set("key2", b"value2")
    await cache.set("key3", b"value3")  # 这应该会移除 key1
    
    value = await cache.get("key1")
    assert value is None  # key1 应该已被移除
    
    value = await cache.get("key2")
    assert value == b"value2"
    
    value = await cache.get("key3")
    assert value == b"value3"

@pytest.mark.asyncio
async def test_cache_concurrent_access():
    """测试并发访问"""
    cache = Cache(max_size=100)
    iterations = 100
    
    async def worker(worker_id: int):
        for i in range(iterations):
            key = f"key_{worker_id}_{i}"
            value = f"value_{worker_id}_{i}".encode()
            await cache.set(key, value)
            result = await cache.get(key)
            assert result == value
    
    # 创建10个并发worker
    workers = [worker(i) for i in range(10)]
    await asyncio.gather(*workers)

@pytest.mark.asyncio
async def test_cache_ttl():
    """测试缓存过期"""
    cache = Cache(max_size=10, ttl=1)  # 1秒TTL
    
    # 设置缓存
    await cache.set("key1", b"value1")
    value = await cache.get("key1")
    assert value == b"value1"
    
    # 等待过期
    await asyncio.sleep(1.1)
    
    # 验证缓存已过期
    value = await cache.get("key1")
    assert value is None

@pytest.mark.asyncio
async def test_cache_clear():
    """测试清空缓存"""
    cache = Cache(max_size=10)
    
    # 添加一些数据
    for i in range(5):
        await cache.set(f"key{i}", f"value{i}".encode())
    
    # 清空缓存
    await cache.clear()
    
    # 验证所有数据都已被清除
    for i in range(5):
        value = await cache.get(f"key{i}")
        assert value is None

@pytest.mark.asyncio
async def test_cache_metrics():
    """测试缓存指标"""
    # 重置指标
    CACHE_OPERATIONS._metrics.clear()
    CACHE_SIZE._value.set(0)
    
    cache = Cache(max_size=10)
    
    # 测试命中和未命中
    await cache.set("key1", b"value1")
    value = await cache.get("key1")  # 命中
    assert value == b"value1"
    
    value = await cache.get("nonexistent")  # 未命中
    assert value is None
    
    # 验证指标
    hits = CACHE_OPERATIONS.labels(operation='hit', status='success')._value.get()
    misses = CACHE_OPERATIONS.labels(operation='miss', status='success')._value.get()
    assert hits == 1
    assert misses == 1
    
    # 测试缓存大小指标
    await cache.set("key2", b"value2")
    size = CACHE_SIZE._value.get()
    assert size == 2
    
    await cache.clear()
    size = CACHE_SIZE._value.get()
    assert size == 0
