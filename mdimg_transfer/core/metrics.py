"""
监控指标模块，提供应用级别的指标收集和导出功能。
"""

import time
from typing import Dict, Optional
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry
from prometheus_client.exposition import generate_latest
import psutil
import asyncio
from functools import wraps

class Metrics:
    """
    应用监控指标管理类，负责收集和导出各类监控指标。
    """
    
    def __init__(self):
        self.registry = CollectorRegistry()
        self._collection_task = None
        
        # 系统指标
        self.memory_usage = Gauge(
            'memory_usage_bytes',
            'Current memory usage in bytes',
            registry=self.registry
        )
        self.cpu_usage = Gauge(
            'cpu_usage_percent',
            'Current CPU usage percentage',
            registry=self.registry
        )
        self.disk_usage = Gauge(
            'disk_usage_bytes',
            'Current disk usage in bytes',
            ['path'],
            registry=self.registry
        )
        
        # 缓存指标
        self.cache_operations = Counter(
            'cache_operations_total',
            'Total number of cache operations',
            ['operation', 'status'],
            registry=self.registry
        )
        self.cache_size = Gauge(
            'cache_size',
            'Current cache size',
            registry=self.registry
        )
        
        # 处理指标
        self.processed_images = Counter(
            'processed_images_total',
            'Total number of processed images',
            ['status'],
            registry=self.registry
        )
        self.processing_duration = Histogram(
            'processing_duration_seconds',
            'Image processing duration in seconds',
            registry=self.registry
        )
        self.processed_bytes = Counter(
            'processed_bytes_total',
            'Total number of processed bytes',
            ['type'],
            registry=self.registry
        )
        
        # 队列指标
        self.queue_size = Gauge(
            'queue_size',
            'Current queue size',
            registry=self.registry
        )
        self.queue_latency = Histogram(
            'queue_latency_seconds',
            'Queue waiting time in seconds',
            registry=self.registry
        )
    
    async def start_metrics_collection(self):
        """启动系统指标收集任务"""
        async def collect_system_metrics():
            while True:
                try:
                    # 收集内存使用情况
                    memory = psutil.Process().memory_info()
                    self.memory_usage.set(memory.rss)
                    
                    # 收集CPU使用情况
                    cpu_percent = psutil.Process().cpu_percent()
                    self.cpu_usage.set(cpu_percent)
                    
                    # 收集磁盘使用情况
                    for partition in psutil.disk_partitions():
                        try:
                            usage = psutil.disk_usage(partition.mountpoint)
                            self.disk_usage.labels(partition.mountpoint).set(usage.used)
                        except Exception:
                            continue
                    
                    await asyncio.sleep(60)  # 每分钟更新一次
                except Exception as e:
                    print(f"Error collecting metrics: {e}")
                    await asyncio.sleep(60)  # 出错时等待一分钟后重试
        
        if self._collection_task is None:
            self._collection_task = asyncio.create_task(collect_system_metrics())
    
    def track_cache_operation(self, operation: str, status: str = "success"):
        """
        记录缓存操作。
        
        Args:
            operation: 操作类型，如 "get", "set", "delete"
            status: 操作状态，如 "success", "error"
        """
        self.cache_operations.labels(operation=operation, status=status).inc()
    
    def update_cache_size(self, size: int):
        """更新缓存大小"""
        self.cache_size.set(size)
    
    def track_image_processing(self, status: str = "success"):
        """记录图片处理"""
        self.processed_images.labels(status=status).inc()
    
    def track_processing_duration(self, duration: float):
        """记录处理时长"""
        self.processing_duration.observe(duration)
    
    def track_processed_bytes(self, bytes_count: int, type_: str = "image"):
        """记录处理的字节数"""
        self.processed_bytes.labels(type=type_).inc(bytes_count)
    
    def update_queue_size(self, size: int):
        """更新队列大小"""
        self.queue_size.set(size)
    
    def track_queue_latency(self, latency: float):
        """记录队列等待时间"""
        self.queue_latency.observe(latency)
    
    def get_metrics(self) -> bytes:
        """导出所有指标"""
        return generate_latest(self.registry)
    
    def get_stats(self) -> Dict[str, float]:
        """获取统计信息"""
        return {
            'memory_usage': self.memory_usage._value.get(),
            'cpu_usage': self.cpu_usage._value.get(),
            'cache_size': self.cache_size._value.get(),
            'queue_size': self.queue_size._value.get(),
        }
    
    def timing(self, metric_name: str):
        """函数执行时间装饰器"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    self.track_processing_duration(time.time() - start_time)
                    return result
                except Exception as e:
                    self.track_processing_duration(time.time() - start_time)
                    raise e
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    self.track_processing_duration(time.time() - start_time)
                    return result
                except Exception as e:
                    self.track_processing_duration(time.time() - start_time)
                    raise e
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

# 全局指标实例
metrics = Metrics()
