"""特定领域的指标收集器"""

import psutil
from typing import Optional
from .metrics import (
    CACHE_SIZE,
    CACHE_OPERATIONS,
    MEMORY_USAGE,
    CPU_USAGE,
    PROCESSED_IMAGES,
    PROCESSED_BYTES,
    QUEUE_SIZE,
    QUEUE_LATENCY,
    DISK_USAGE,
    WORKER_COUNT,
    WORKER_BUSY,
)

class SystemMetrics:
    """系统资源指标管理器"""
    
    @staticmethod
    def update_metrics():
        """更新系统资源指标"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        
        MEMORY_USAGE.set(memory.used)
        CPU_USAGE.set(cpu)
    
    @staticmethod
    def get_current_usage():
        """获取当前资源使用情况"""
        return {
            'memory_used': MEMORY_USAGE._value.get(),
            'cpu_percent': CPU_USAGE._value.get()
        }

class ResourceCollector:
    """系统资源收集器"""
    
    @staticmethod
    def update_resource_metrics():
        """更新系统资源指标"""
        import psutil
        
        # 更新内存使用
        memory = psutil.Process().memory_info()
        MEMORY_USAGE.set(memory.rss)
        
        # 更新CPU使用
        CPU_USAGE.set(psutil.Process().cpu_percent())
        
        # 更新磁盘使用
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                DISK_USAGE.labels(path=partition.mountpoint).set(usage.used)
            except Exception:
                continue

class CacheMetrics:
    """缓存指标管理器"""
    
    @staticmethod
    def update_size(size: int):
        """更新缓存大小"""
        CACHE_SIZE.set(size)
    
    @staticmethod
    def record_hit():
        """记录缓存命中"""
        CACHE_OPERATIONS.labels(operation='hit', status='success').inc()
    
    @staticmethod
    def record_miss():
        """记录缓存未命中"""
        CACHE_OPERATIONS.labels(operation='miss', status='success').inc()
    
    @staticmethod
    def record_error(operation: str):
        """记录缓存错误"""
        CACHE_OPERATIONS.labels(operation=operation, status='error').inc()

class WorkerCollector:
    """工作进程指标收集器"""
    
    @staticmethod
    def update_worker_metrics(total: int, busy: int):
        """更新工作进程指标"""
        WORKER_COUNT.set(total)
        WORKER_BUSY.set(busy)

class QueueCollector:
    """队列指标收集器"""
    
    @staticmethod
    def record_queue_size(size: int):
        """记录队列大小"""
        QUEUE_SIZE.set(size)
    
    @staticmethod
    def record_queue_latency(duration: float):
        """记录队列等待时间"""
        QUEUE_LATENCY.observe(duration)

class ProcessingMetrics:
    """图片处理指标管理器"""
    
    @staticmethod
    def record_processing_time(duration: float):
        """记录处理时间"""
        QUEUE_LATENCY.observe(duration)
    
    @staticmethod
    def record_success():
        """记录处理成功"""
        PROCESSED_IMAGES.labels(status='success', error_type='none').inc()
    
    @staticmethod
    def record_error(error_type: str = 'unknown'):
        """记录处理错误"""
        PROCESSED_IMAGES.labels(status='failed', error_type=error_type).inc()
    
    @staticmethod
    def record_image_size(size: int, image_type: str):
        """记录图片大小"""
        PROCESSED_BYTES.labels(type='processed', format=image_type).inc(size)
    
    @staticmethod
    def record_queue_size(size: int):
        """记录队列大小"""
        QUEUE_SIZE.set(size)
    
    @staticmethod
    def record_queue_latency(duration: float):
        """记录队列等待时间"""
        QUEUE_LATENCY.observe(duration)
    
    @staticmethod
    def get_current_metrics():
        """获取当前处理指标"""
        return {
            'queue_size': QUEUE_SIZE._value.get(),
            'processed_images': sum(
                PROCESSED_IMAGES.collect()[0].samples[0].value
                for m in PROCESSED_IMAGES.collect()
            )
        }
