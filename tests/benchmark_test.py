"""性能基准测试模块"""

import pytest
import asyncio
import time
from typing import List
import io
from PIL import Image
from mdimg_transfer.core.image_processing import ImageProcessor, ImageConfig
from mdimg_transfer.core.cache import AsyncLRUCache
from mdimg_transfer.errors.retry import RetryConfig, with_retry

def create_test_image(width: int, height: int) -> bytes:
    """创建测试图片"""
    image = Image.new('RGB', (width, height), color='red')
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG', quality=95)
    return image_bytes.getvalue()

@pytest.mark.benchmark
async def test_image_processing_performance(benchmark):
    """测试图片处理性能"""
    # 准备测试数据
    test_images = [
        create_test_image(1920, 1080),  # 1080p
        create_test_image(3840, 2160),  # 4K
        create_test_image(1280, 720),   # 720p
    ]
    
    processor = ImageProcessor()
    config = ImageConfig(max_width=800, max_height=600)
    
    async def process_batch(images: List[bytes]):
        tasks = [processor.process_image(img, config) for img in images]
        return await asyncio.gather(*tasks)
    
    # 运行基准测试
    results = benchmark(lambda: asyncio.run(process_batch(test_images)))
    assert len(results) == len(test_images)

@pytest.mark.benchmark
async def test_cache_performance(benchmark):
    """测试缓存性能"""
    cache = AsyncLRUCache(max_size=1000)
    test_data = [(f"key_{i}", f"value_{i}") for i in range(1000)]
    
    async def cache_operations():
        # 写入
        for key, value in test_data:
            await cache.set(key, value)
        
        # 读取
        for key, _ in test_data:
            await cache.get(key)
    
    # 运行基准测试
    benchmark(lambda: asyncio.run(cache_operations()))
    assert cache.hits + cache.misses == len(test_data)

@pytest.mark.benchmark
async def test_concurrent_processing_performance(benchmark):
    """测试并发处理性能"""
    processor = ImageProcessor()
    config = ImageConfig(max_width=800, max_height=600)
    
    # 创建不同大小的测试图片
    test_images = [
        create_test_image(1920, 1080) for _ in range(10)
    ]
    
    async def process_concurrent(concurrency: int):
        semaphore = asyncio.Semaphore(concurrency)
        async def process_with_limit(img: bytes):
            async with semaphore:
                return await processor.process_image(img, config)
        
        tasks = [process_with_limit(img) for img in test_images]
        return await asyncio.gather(*tasks)
    
    # 测试不同并发级别
    concurrency_levels = [1, 2, 4, 8]
    for concurrency in concurrency_levels:
        results = benchmark(
            lambda: asyncio.run(process_concurrent(concurrency)),
            name=f"concurrent_processing_{concurrency}"
        )
        assert len(results) == len(test_images)

@pytest.mark.benchmark
async def test_retry_performance(benchmark):
    """测试重试机制性能"""
    retry_config = RetryConfig(max_retries=3, delay=0.1)
    failure_count = 0
    
    @with_retry(retry_config)
    async def flaky_operation():
        nonlocal failure_count
        failure_count += 1
        if failure_count % 2 == 0:
            return "success"
        raise ConnectionError("Simulated failure")
    
    # 运行基准测试
    benchmark(lambda: asyncio.run(flaky_operation()))

if __name__ == '__main__':
    pytest.main(['-v', '--benchmark-only'])
