"""基础指标定义"""

import time
from typing import Dict, Optional
from dataclasses import dataclass
from contextlib import contextmanager
from prometheus_client import Counter, Histogram, Gauge, Summary, Info

@dataclass
class ProcessingStats:
    """图片处理统计信息"""
    original_size: int
    processed_size: int
    processing_time: float
    compression_ratio: float
    error: Optional[str] = None

# 系统信息
SYSTEM_INFO = Info('mdimg_system', '系统信息')
SYSTEM_INFO.info({
    'version': '0.1.0',
    'python_version': '3.10'
})

# 请求指标
REQUEST_COUNT = Counter(
    'mdimg_requests_total',
    '请求总数',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'mdimg_request_duration_seconds',
    '请求处理时间',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# 图片处理指标
PROCESSED_IMAGES = Counter(
    'mdimg_processed_images_total',
    'Total number of processed images',
    ['status', 'error_type']
)

PROCESSED_BYTES = Counter(
    'mdimg_processed_bytes_total',
    'Total bytes of processed images',
    ['type', 'format']
)

IMAGE_SIZE = Histogram(
    'mdimg_image_size_bytes',
    '图片大小分布',
    ['type'],
    buckets=[1024, 10*1024, 100*1024, 1024*1024, 10*1024*1024]
)

PROCESSING_ERRORS = Counter(
    'mdimg_processing_errors_total',
    '处理错误数',
    ['type']
)

THROUGHPUT = Counter(
    'mdimg_throughput_bytes',
    '处理吞吐量',
    ['direction']  # 'input' 或 'output'
)

COMPRESSION_RATIO = Histogram(
    'mdimg_compression_ratio',
    '压缩比率',
    buckets=[0.1, 0.3, 0.5, 0.7, 0.9]
)

# 处理时间指标
PROCESSING_TIME = Histogram(
    'mdimg_processing_duration_seconds',
    'Time spent processing images',
    ['operation'],  # operation: total/io/processing/optimization
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

# 磁盘IO指标
DISK_IO = Counter(
    'mdimg_disk_io_bytes',
    'Total disk I/O bytes',
    ['operation']  # operation: read/write
)

# 磁盘使用指标
DISK_USAGE = Gauge(
    'mdimg_disk_usage_bytes',
    'Current disk usage in bytes',
    ['path']  # path: cache/temp/output
)

# 当前处理指标
CURRENT_PROCESSING = Gauge(
    'mdimg_current_processing',
    'Number of images currently being processed',
    ['state']  # state: waiting/processing/saving
)

# 缓存指标
CACHE_SIZE = Gauge(
    'mdimg_cache_size_bytes',
    'Current cache size in bytes'
)

CACHE_OPERATIONS = Counter(
    'mdimg_cache_operations_total',
    'Cache operations count',
    ['operation', 'status']  # operation: hit/miss/error
)

# 资源使用指标
MEMORY_USAGE = Gauge(
    'mdimg_memory_usage_bytes',
    'Current memory usage in bytes'
)

CPU_USAGE = Gauge(
    'mdimg_cpu_usage_percent',
    'Current CPU usage percentage'
)

# 队列指标
QUEUE_SIZE = Gauge(
    'mdimg_queue_size',
    'Current queue size'
)

QUEUE_LATENCY = Histogram(
    'mdimg_queue_wait_time_seconds',
    'Queue wait time in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# 工作进程指标
WORKER_COUNT = Gauge(
    'mdimg_worker_count',
    'Number of active worker processes',
    ['type']  # type: total/busy/idle
)

WORKER_BUSY = Gauge(
    'mdimg_workers_busy',
    'Number of busy workers'
)

class MetricsCollector:
    """统一的指标收集器"""
    
    def __init__(self):
        self._start_times: Dict[str, float] = {}
    
    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """记录HTTP请求"""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_processed_image(self, stats: ProcessingStats, image_format: str):
        """记录已处理的图片统计信息"""
        status = 'success' if not stats.error else 'failed'
        error_type = 'none' if not stats.error else 'processing_error'
        
        PROCESSED_IMAGES.labels(status=status, error_type=error_type).inc()
        PROCESSED_BYTES.labels(type='original', format=image_format).inc(stats.original_size)
        PROCESSED_BYTES.labels(type='processed', format=image_format).inc(stats.processed_size)
        IMAGE_SIZE.labels(type='original').observe(stats.original_size)
        IMAGE_SIZE.labels(type='processed').observe(stats.processed_size)
        if stats.error:
            PROCESSING_ERRORS.labels(type='processing_error').inc()
        THROUGHPUT.labels(direction='input').inc(stats.original_size)
        THROUGHPUT.labels(direction='output').inc(stats.processed_size)
        COMPRESSION_RATIO.observe(stats.compression_ratio)
    
    @contextmanager
    def track_processing_time(self, operation: str = 'total'):
        """跟踪处理时间的上下文管理器"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(method='process', endpoint=operation).observe(duration)
            PROCESSING_TIME.labels(operation=operation).observe(duration)
    
    def update_resource_usage(self, memory_bytes: int, cpu_percent: float):
        """更新资源使用情况"""
        MEMORY_USAGE.set(memory_bytes)
        CPU_USAGE.set(cpu_percent)
    
    def update_queue_metrics(self, size: int, wait_time: float):
        """更新队列指标"""
        QUEUE_SIZE.set(size)
        QUEUE_LATENCY.observe(wait_time)
    
    def update_disk_io(self, operation: str, bytes_count: int):
        """更新磁盘IO指标"""
        DISK_IO.labels(operation=operation).inc(bytes_count)
    
    def update_current_processing(self, state: str, count: int):
        """更新当前处理指标"""
        CURRENT_PROCESSING.labels(state=state).set(count)
    
    def update_disk_usage(self, path: str, usage_bytes: int):
        """更新磁盘使用指标"""
        DISK_USAGE.labels(path=path).set(usage_bytes)

    def update_worker_count(self, type_: str, count: int):
        """更新工作进程数量"""
        WORKER_COUNT.labels(type=type_).set(count)
