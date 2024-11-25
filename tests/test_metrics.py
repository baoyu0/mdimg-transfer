"""
监控指标模块的测试用例。
"""

import pytest
import asyncio
from mdimg_transfer.core.metrics import Metrics

@pytest.fixture
def metrics():
    return Metrics()

def test_track_cache_operation(metrics):
    """测试缓存操作指标"""
    metrics.track_cache_operation("get", "success")
    metrics.track_cache_operation("get", "miss")
    metrics.track_cache_operation("set", "success")
    
    stats = metrics.get_stats()
    assert stats["cache_hit_rate"] == 50.0  # 一次命中，一次未命中

def test_update_cache_size(metrics):
    """测试缓存大小指标"""
    metrics.update_cache_size(100)
    assert metrics.cache_size._value.get() == 100

def test_track_image_processing(metrics):
    """测试图片处理指标"""
    metrics.track_image_processing("success")
    metrics.track_image_processing("error")
    
    stats = metrics.get_stats()
    assert stats["total_processed"] == 2
    assert stats["success_rate"] == 50.0

def test_track_processed_bytes(metrics):
    """测试处理字节数指标"""
    metrics.track_processed_bytes(1000, "image")
    metrics.track_processed_bytes(500, "markdown")
    
    stats = metrics.get_stats()
    assert stats["total_bytes_processed"] == 1500

def test_update_queue_size(metrics):
    """测试队列大小指标"""
    metrics.update_queue_size(5)
    assert metrics.queue_size._value.get() == 5

def test_track_queue_latency(metrics):
    """测试队列延迟指标"""
    metrics.track_queue_latency(0.5)
    metrics.track_queue_latency(1.0)
    
    # 验证直方图数据
    assert sum(metrics.queue_latency._count.values()) == 2
    assert sum(metrics.queue_latency._sum.values()) == 1.5

@pytest.mark.asyncio
async def test_time_processing_decorator(metrics):
    """测试处理时间装饰器"""
    @metrics.time_processing
    async def mock_processing():
        await asyncio.sleep(0.1)
        return True
    
    result = await mock_processing()
    assert result is True
    
    stats = metrics.get_stats()
    assert stats["average_processing_time"] >= 0.1

@pytest.mark.asyncio
async def test_time_processing_decorator_error(metrics):
    """测试处理时间装饰器（错误情况）"""
    @metrics.time_processing
    async def mock_processing_error():
        await asyncio.sleep(0.1)
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        await mock_processing_error()
    
    stats = metrics.get_stats()
    assert stats["success_rate"] == 0.0

def test_get_metrics_format(metrics):
    """测试指标导出格式"""
    metrics.track_image_processing("success")
    metrics.update_cache_size(100)
    
    metrics_data = metrics.get_metrics()
    assert isinstance(metrics_data, bytes)
    metrics_text = metrics_data.decode('utf-8')
    
    # 验证指标格式
    assert 'processed_images_total{status="success"} 1.0' in metrics_text
    assert 'cache_size 100.0' in metrics_text

def test_system_metrics_initialization(metrics):
    """测试系统指标初始化"""
    # 验证系统指标是否正确初始化
    assert metrics.memory_usage._value is not None
    assert metrics.cpu_usage._value is not None
    
    # 验证磁盘指标
    metrics_data = metrics.get_metrics().decode('utf-8')
    assert 'disk_usage_bytes{path=' in metrics_data

def test_stats_calculation_empty(metrics):
    """测试统计信息计算（空数据）"""
    stats = metrics.get_stats()
    
    # 验证空数据时的默认值
    assert stats["total_processed"] == 0
    assert stats["success_rate"] == 100.0
    assert stats["average_processing_time"] == 0.0
    assert stats["total_bytes_processed"] == 0
    assert stats["cache_hit_rate"] == 100.0

def test_stats_calculation_with_data(metrics):
    """测试统计信息计算（有数据）"""
    # 添加测试数据
    metrics.track_image_processing("success")
    metrics.track_image_processing("success")
    metrics.track_image_processing("error")
    
    metrics.track_cache_operation("get", "success")
    metrics.track_cache_operation("get", "success")
    metrics.track_cache_operation("get", "miss")
    
    metrics.track_processed_bytes(1000, "image")
    
    metrics.track_queue_latency(0.5)
    metrics.track_queue_latency(1.5)
    
    # 验证统计结果
    stats = metrics.get_stats()
    assert stats["total_processed"] == 3
    assert stats["success_rate"] == pytest.approx(66.67, rel=1e-2)
    assert stats["cache_hit_rate"] == pytest.approx(66.67, rel=1e-2)
    assert stats["total_bytes_processed"] == 1000
