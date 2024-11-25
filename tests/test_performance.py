"""性能测试模块"""

import asyncio
import io
import os
import time
from pathlib import Path

import pytest
from PIL import Image

from mdimg_transfer.core.cache import Cache
from mdimg_transfer.core.image_processing import ImageProcessor

TEST_IMAGE_SIZE = (1920, 1080)
TEST_IMAGE_COUNT = 10

@pytest.fixture
def test_images():
    """生成测试图片"""
    images = []
    for _ in range(TEST_IMAGE_COUNT):
        # 创建测试图片
        img = Image.new('RGB', TEST_IMAGE_SIZE, color='red')
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95)
        images.append(output.getvalue())
    return images

@pytest.mark.asyncio
async def test_image_processing_performance(test_images):
    """测试图片处理性能"""
    processor = ImageProcessor()

    # 测试单张图片处理
    start_time = time.time()
    result = await processor.process_image(test_images[0])
    single_time = time.time() - start_time
    
    assert len(result) > 0
    print(f"\nSingle image processing time: {single_time:.2f}s")

    # 测试并发处理多张图片
    start_time = time.time()
    results = await processor.process_images(test_images)
    batch_time = time.time() - start_time

    assert len(results) == len(test_images)
    print(f"Batch processing time ({len(test_images)} images): {batch_time:.2f}s")
    print(f"Average time per image in batch: {batch_time/len(test_images):.2f}s")

    # 验证性能提升
    theoretical_serial_time = single_time * len(test_images)
    speedup = theoretical_serial_time / batch_time
    print(f"Speedup factor: {speedup:.2f}x")

    processor.close()

@pytest.mark.asyncio
async def test_cache_performance():
    """测试缓存性能"""
    cache = Cache(max_size=1000)
    test_data = b"test" * 1000  # 4KB of test data
    iterations = 1000

    # 测试写入性能
    start_time = time.time()
    for i in range(iterations):
        await cache.set(f"key{i}", test_data)
    write_time = time.time() - start_time
    print(f"\nCache write time ({iterations} items): {write_time:.2f}s")
    print(f"Average write time: {write_time/iterations*1000:.2f}ms")

    # 测试读取性能
    start_time = time.time()
    for i in range(iterations):
        await cache.get(f"key{i}")
    read_time = time.time() - start_time
    print(f"Cache read time ({iterations} items): {read_time:.2f}s")
    print(f"Average read time: {read_time/iterations*1000:.2f}ms")

    # 测试缓存命中率
    hits = misses = 0
    for i in range(iterations * 2):  # 测试更多次以包含未缓存的key
        result = await cache.get(f"key{i}")
        if result is not None:
            hits += 1
        else:
            misses += 1
    
    hit_rate = hits / (hits + misses)
    print(f"Cache hit rate: {hit_rate*100:.1f}%")

@pytest.mark.asyncio
async def test_concurrent_cache_access():
    """测试并发缓存访问"""
    cache = Cache(max_size=1000)
    test_data = b"test" * 100
    iterations = 100
    concurrent_users = 10

    async def worker(worker_id: int):
        for i in range(iterations):
            key = f"key{worker_id}_{i}"
            await cache.set(key, test_data)
            await cache.get(key)

    # 并发执行多个worker
    start_time = time.time()
    workers = [worker(i) for i in range(concurrent_users)]
    await asyncio.gather(*workers)
    total_time = time.time() - start_time

    operations = concurrent_users * iterations * 2  # 每次迭代包含一次读和一次写
    print(f"\nConcurrent cache operations ({operations} total):")
    print(f"Total time: {total_time:.2f}s")
    print(f"Operations per second: {operations/total_time:.0f}")
