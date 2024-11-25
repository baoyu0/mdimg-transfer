"""性能分析测试"""

import asyncio
import os
import pytest
from PIL import Image
import io
import time

from mdimg_transfer.monitoring.profiler import AsyncProfiler, profile_async, PerformanceReport
from mdimg_transfer.core.image_processing import ImageProcessor
from mdimg_transfer.core.cache import AsyncLRUCache

def create_test_image(size=(800, 600), color='white'):
    """创建测试图片"""
    img = Image.new('RGB', size, color=color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

@pytest.mark.asyncio
@profile_async(name="test_image_processing_profiling")
async def test_image_processing_profiling():
    """测试图片处理性能分析"""
    # 创建处理器和报告生成器
    processor = ImageProcessor()
    report = PerformanceReport()
    
    # 预热处理器
    await processor.warmup()
    
    # 创建不同大小的测试图片
    images = [
        create_test_image((800, 600)),  # 小图
        create_test_image((1600, 1200)),  # 中图
        create_test_image((3200, 2400))  # 大图
    ]
    
    # 测试不同大小图片的处理性能
    for i, image in enumerate(images):
        size_label = ['small', 'medium', 'large'][i]
        
        # 执行多次处理并记录性能
        for _ in range(5):
            start_time = time.time()
            processed_image = await processor.process_image(image)
            duration = time.time() - start_time
            report.record_metric(f"image_processing_time_{size_label}", duration)
            
            assert processed_image is not None
            assert len(processed_image) > 0
    
    # 保存性能报告
    report.save_report("image_processing_report.txt")

@pytest.mark.asyncio
@profile_async(name="test_cache_profiling")
async def test_cache_profiling():
    """测试缓存性能分析"""
    # 创建缓存和报告生成器
    cache = AsyncLRUCache(max_size=1000)
    report = PerformanceReport()
    
    # 测试写入性能
    start_time = time.time()
    for i in range(1000):
        key = f"key_{i}"
        value = "x" * (1024 * i % 10240)  # 变化的数据大小
        await cache.set(key, value)
    write_time = time.time() - start_time
    report.record_metric("bulk_write_time", write_time)
    
    # 测试读取性能
    start_time = time.time()
    for i in range(1000):
        key = f"key_{i}"
        value = await cache.get(key)
        assert value is not None
    read_time = time.time() - start_time
    report.record_metric("bulk_read_time", read_time)
    
    # 测试缓存淘汰
    start_time = time.time()
    for i in range(2000):  # 超过缓存大小
        key = f"new_key_{i}"
        value = "x" * 1024
        await cache.set(key, value)
    eviction_time = time.time() - start_time
    report.record_metric("cache_eviction_time", eviction_time)
    
    # 保存性能报告
    report.save_report("cache_report.txt")

@pytest.mark.asyncio
async def test_concurrent_operations_profiling():
    """测试并发操作性能分析"""
    processor = ImageProcessor()
    cache = AsyncLRUCache(max_size=1000)
    report = PerformanceReport()
    
    # 预热处理器
    await processor.warmup()
    
    # 创建不同大小的测试图片
    images = [
        create_test_image((800, 600), 'red'),
        create_test_image((1600, 1200), 'green'),
        create_test_image((3200, 2400), 'blue')
    ]
    
    async def process_and_cache(image_data: bytes, label: str):
        """处理图片并缓存"""
        start_time = time.time()
        
        # 处理图片
        processed_image = await processor.process_image(image_data)
        
        # 缓存结果
        key = f"image_{label}_{time.time()}"
        await cache.set(key, processed_image)
        
        duration = time.time() - start_time
        report.record_metric(f"concurrent_operation_time_{label}", duration)
        
        return processed_image
    
    # 创建并发任务 - 每种大小的图片处理5次
    tasks = []
    for i, image in enumerate(images):
        size_label = ['small', 'medium', 'large'][i]
        for j in range(5):
            task = process_and_cache(image, f"{size_label}_{j}")
            tasks.append(task)
    
    # 执行并发任务
    results = await asyncio.gather(*tasks)
    
    # 验证结果
    for result in results:
        assert result is not None
        assert len(result) > 0
    
    # 保存性能报告
    report.save_report("concurrent_operations_report.txt")

@pytest.mark.asyncio
async def test_worker_adjustment():
    """测试工作进程数自动调整"""
    processor = ImageProcessor(
        max_workers=4,
        min_workers=2,
        max_chunk_size=1024 * 1024
    )
    report = PerformanceReport()
    
    # 预热处理器
    await processor.warmup()
    
    # 创建大量测试图片
    images = [create_test_image((1600, 1200)) for _ in range(20)]
    
    # 并发处理图片
    start_time = time.time()
    results = await processor.process_images(images)
    duration = time.time() - start_time
    
    # 记录性能指标
    report.record_metric("batch_processing_time", duration)
    report.record_metric("average_time_per_image", duration / len(images))
    
    # 验证结果
    for result in results:
        assert result is not None
        assert len(result) > 0
    
    # 保存性能报告
    report.save_report("worker_adjustment_report.txt")
