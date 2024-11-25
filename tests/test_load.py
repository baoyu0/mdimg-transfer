"""负载测试模块"""

import asyncio
import io
import random
import time
from typing import List, Tuple

import pytest
from PIL import Image

from mdimg_transfer.core.image_processing import ImageProcessor
from mdimg_transfer.core.cache import Cache

async def simulate_user_behavior(
    processor: ImageProcessor,
    cache: Cache,
    image_data: bytes,
    iterations: int
) -> Tuple[float, float, int]:
    """
    模拟用户行为

    Args:
        processor: 图片处理器
        cache: 缓存
        image_data: 测试图片数据
        iterations: 迭代次数

    Returns:
        平均响应时间, 95th百分位响应时间, 错误数
    """
    response_times = []
    errors = 0

    for _ in range(iterations):
        try:
            # 随机选择图片大小和质量
            max_size = random.choice([(800, 800), (400, 400), (200, 200)])
            quality = random.randint(60, 95)

            # 生成缓存键
            cache_key = f"img_{max_size}_{quality}"

            # 检查缓存
            start_time = time.time()
            result = await cache.get(cache_key)

            if result is None:
                # 处理图片
                result = await processor.process_image(
                    image_data,
                    max_size=max_size,
                    quality=quality
                )
                await cache.set(cache_key, result)

            response_time = time.time() - start_time
            response_times.append(response_time)

            # 模拟用户思考时间
            await asyncio.sleep(random.uniform(0.1, 0.5))

        except Exception:
            errors += 1

    if not response_times:
        return 0.0, 0.0, errors

    avg_time = sum(response_times) / len(response_times)
    p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
    
    return avg_time, p95_time, errors

@pytest.fixture
def test_image():
    """生成测试图片"""
    img = Image.new('RGB', (1920, 1080), color='red')
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=95)
    return output.getvalue()

@pytest.mark.asyncio
async def test_load(test_image):
    """负载测试"""
    # 测试参数
    concurrent_users = [1, 5, 10, 20, 50]
    iterations_per_user = 20
    warmup_time = 5  # 预热时间(秒)

    processor = ImageProcessor()
    cache = Cache(max_size=1000)

    print("\n负载测试结果:")
    print("并发用户数 | 平均响应时间(ms) | 95th响应时间(ms) | 错误率 | RPS")
    print("-" * 65)

    for num_users in concurrent_users:
        # 创建用户任务
        tasks = [
            simulate_user_behavior(
                processor,
                cache,
                test_image,
                iterations_per_user
            )
            for _ in range(num_users)
        ]

        # 预热
        await asyncio.sleep(warmup_time)

        # 执行负载测试
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # 统计结果
        avg_times, p95_times, errors = zip(*results)
        overall_avg = sum(avg_times) / len(avg_times)
        overall_p95 = max(p95_times)
        total_errors = sum(errors)
        total_requests = num_users * iterations_per_user
        error_rate = total_errors / total_requests * 100
        rps = total_requests / total_time

        print(
            f"{num_users:^11d} | "
            f"{overall_avg*1000:^14.2f} | "
            f"{overall_p95*1000:^15.2f} | "
            f"{error_rate:^6.1f}% | "
            f"{rps:^4.1f}"
        )

    processor.close()

@pytest.mark.asyncio
async def test_stress():
    """压力测试"""
    processor = ImageProcessor()
    cache = Cache(max_size=1000)

    # 生成大量测试数据
    test_data = []
    for size in [(1920, 1080), (3840, 2160), (800, 600)]:
        img = Image.new('RGB', size, color='red')
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95)
        test_data.append(output.getvalue())

    # 测试参数
    duration = 60  # 测试持续时间(秒)
    max_concurrent = 100  # 最大并发请求数

    print("\n压力测试结果:")
    start_time = time.time()
    request_count = 0
    error_count = 0

    async def stress_worker():
        nonlocal request_count, error_count
        while time.time() - start_time < duration:
            try:
                # 随机选择测试数据和参数
                image_data = random.choice(test_data)
                max_size = random.choice([(800, 800), (400, 400), (200, 200)])
                quality = random.randint(60, 95)

                # 处理图片
                await processor.process_image(
                    image_data,
                    max_size=max_size,
                    quality=quality
                )
                request_count += 1

            except Exception:
                error_count += 1

            # 随机延迟
            await asyncio.sleep(random.uniform(0.01, 0.1))

    # 创建worker任务
    workers = [stress_worker() for _ in range(max_concurrent)]
    await asyncio.gather(*workers)

    total_time = time.time() - start_time
    rps = request_count / total_time
    error_rate = error_count / (request_count + error_count) * 100

    print(f"测试持续时间: {total_time:.1f}秒")
    print(f"总请求数: {request_count}")
    print(f"平均RPS: {rps:.1f}")
    print(f"错误数: {error_count}")
    print(f"错误率: {error_rate:.1f}%")

    processor.close()
