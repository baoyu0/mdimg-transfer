# 性能优化指南

本文档详细说明了 Markdown Image Transfer 工具的性能优化策略和最佳实践。

## 1. 并行处理优化

### 1.1 动态并发控制

```python
class DynamicConcurrencyManager:
    def __init__(self, initial_concurrency: int = 4):
        self.current_concurrency = initial_concurrency
        self.performance_metrics = []
        
    async def adjust_concurrency(self, metrics: Dict[str, float]):
        """根据性能指标动态调整并发数"""
        cpu_usage = metrics['cpu_usage']
        memory_usage = metrics['memory_usage']
        
        if cpu_usage > 80 or memory_usage > 85:
            self.current_concurrency = max(2, self.current_concurrency - 1)
        elif cpu_usage < 50 and memory_usage < 60:
            self.current_concurrency = min(8, self.current_concurrency + 1)
            
        return self.current_concurrency
```

### 1.2 任务分组和批处理

```python
async def process_in_batches(items: List[str], batch_size: int = 4):
    """分批处理任务"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [process_item(item) for item in batch]
        await asyncio.gather(*tasks)
```

## 2. 内存优化

### 2.1 图片处理内存优化

```python
from PIL import Image
import io

async def optimize_image_memory(image_path: str, max_size: int = 1024):
    """内存优化的图片处理"""
    with Image.open(image_path) as img:
        # 计算新尺寸
        ratio = min(max_size / max(img.size), 1.0)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        
        # 使用缩略图减少内存使用
        img.thumbnail(new_size, Image.LANCZOS)
        
        # 使用BytesIO避免临时文件
        buf = io.BytesIO()
        img.save(buf, format='JPEG', optimize=True)
        return buf.getvalue()
```

### 2.2 流式处理大文件

```python
async def process_large_markdown(file_path: str, chunk_size: int = 8192):
    """流式处理大型Markdown文件"""
    async with aiofiles.open(file_path, 'r') as f:
        buffer = []
        async for line in f:
            buffer.append(line)
            if len(buffer) >= chunk_size:
                await process_chunk(buffer)
                buffer = []
        if buffer:
            await process_chunk(buffer)
```

## 3. 缓存优化

### 3.1 多级缓存策略

```python
from functools import lru_cache
import aioredis

class CacheManager:
    def __init__(self):
        self.memory_cache = {}
        self.redis = aioredis.from_url("redis://localhost")
        
    @lru_cache(maxsize=1000)
    def get_from_memory(self, key: str):
        """内存缓存"""
        return self.memory_cache.get(key)
        
    async def get_from_redis(self, key: str):
        """Redis缓存"""
        return await self.redis.get(key)
        
    async def get_cached_data(self, key: str):
        """多级缓存获取"""
        # 先查内存缓存
        data = self.get_from_memory(key)
        if data:
            return data
            
        # 再查Redis缓存
        data = await self.get_from_redis(key)
        if data:
            self.memory_cache[key] = data
            return data
            
        # 缓存未命中，从源获取
        data = await fetch_from_source(key)
        await self.cache_data(key, data)
        return data
```

### 3.2 智能缓存失效

```python
class SmartCache:
    def __init__(self):
        self.cache = {}
        self.access_count = Counter()
        self.last_access = {}
        
    def should_cache(self, key: str, size: int) -> bool:
        """智能判断是否应该缓存"""
        access_frequency = self.access_count[key]
        last_access_time = self.last_access.get(key, 0)
        time_since_last_access = time.time() - last_access_time
        
        # 根据访问频率、数据大小和上次访问时间决定是否缓存
        score = access_frequency / (size * time_since_last_access)
        return score > 0.1
```

## 4. 网络优化

### 4.1 连接池管理

```python
class ConnectionPool:
    def __init__(self, max_size: int = 100):
        self.pool = []
        self.max_size = max_size
        self.semaphore = asyncio.Semaphore(max_size)
        
    async def get_connection(self):
        """获取连接"""
        async with self.semaphore:
            if self.pool:
                return self.pool.pop()
            return await create_connection()
            
    async def release_connection(self, conn):
        """释放连接"""
        if len(self.pool) < self.max_size:
            self.pool.append(conn)
        else:
            await conn.close()
```

### 4.2 智能重试策略

```python
class SmartRetry:
    def __init__(self):
        self.failure_count = Counter()
        self.last_failure = {}
        
    async def should_retry(self, operation: str, error: Exception) -> bool:
        """智能判断是否应该重试"""
        current_time = time.time()
        failure_count = self.failure_count[operation]
        last_failure_time = self.last_failure.get(operation, 0)
        
        # 指数退避
        if current_time - last_failure_time < (2 ** failure_count):
            return False
            
        # 根据错误类型判断
        if isinstance(error, (ConnectionError, TimeoutError)):
            return True
        return False
```

## 5. 资源管理

### 5.1 系统资源监控

```python
import psutil

class ResourceMonitor:
    def __init__(self, threshold_cpu: float = 80, threshold_memory: float = 85):
        self.threshold_cpu = threshold_cpu
        self.threshold_memory = threshold_memory
        
    def get_system_metrics(self) -> Dict[str, float]:
        """获取系统指标"""
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()
        }
        
    def is_system_healthy(self) -> bool:
        """检查系统健康状态"""
        metrics = self.get_system_metrics()
        return (metrics['cpu_usage'] < self.threshold_cpu and 
                metrics['memory_usage'] < self.threshold_memory)
```

### 5.2 资源自动释放

```python
class ResourceManager:
    def __init__(self):
        self.temp_files = set()
        self.open_connections = set()
        
    async def cleanup(self):
        """清理资源"""
        # 清理临时文件
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except OSError as e:
                logger.warning(f"清理临时文件失败: {e}")
                
        # 关闭连接
        for conn in self.open_connections:
            try:
                await conn.close()
            except Exception as e:
                logger.warning(f"关闭连接失败: {e}")
```

## 6. 性能监控和分析

### 6.1 性能指标收集

```python
class PerformanceMetrics:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    async def record_metric(self, name: str, value: float):
        """记录性能指标"""
        self.metrics[name].append({
            'value': value,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_average(self, name: str, minutes: int = 5) -> float:
        """获取平均值"""
        recent = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [
            m['value'] for m in self.metrics[name]
            if datetime.fromisoformat(m['timestamp']) > recent
        ]
        return sum(recent_metrics) / len(recent_metrics) if recent_metrics else 0
```

### 6.2 性能报告生成

```python
class PerformanceReport:
    def __init__(self, metrics: PerformanceMetrics):
        self.metrics = metrics
        
    def generate_report(self) -> Dict[str, Any]:
        """生成性能报告"""
        return {
            'summary': {
                'avg_processing_time': self.metrics.get_average('processing_time'),
                'avg_memory_usage': self.metrics.get_average('memory_usage'),
                'avg_cpu_usage': self.metrics.get_average('cpu_usage')
            },
            'recommendations': self.generate_recommendations(),
            'alerts': self.check_alerts()
        }
```

## 7. 最佳实践建议

1. **合理设置批处理大小**
   - 根据系统资源和负载动态调整
   - 监控处理时间和资源使用

2. **使用异步操作**
   - 对I/O密集型操作使用异步
   - 合理控制并发数量

3. **实现优雅降级**
   - 设置服务降级阈值
   - 提供备选处理方案

4. **定期清理资源**
   - 及时释放不需要的内存
   - 清理临时文件和缓存

5. **监控系统指标**
   - 设置关键指标告警
   - 定期生成性能报告

## 8. 性能调优检查清单

- [ ] 是否实现了动态并发控制？
- [ ] 是否使用了合适的缓存策略？
- [ ] 是否实现了资源监控和告警？
- [ ] 是否有完善的错误处理和重试机制？
- [ ] 是否定期清理临时资源？
- [ ] 是否实现了性能指标收集和分析？
- [ ] 是否有服务降级方案？
- [ ] 是否优化了大文件处理？
