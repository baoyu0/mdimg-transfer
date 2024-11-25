# 错误处理指南

本文档详细说明了 Markdown Image Transfer 工具中的错误处理机制和最佳实践。

## 错误类型

### 1. 输入验证错误

```python
class ValidationError(Exception):
    """输入验证错误的基类"""
    pass

class InvalidFileType(ValidationError):
    """不支持的文件类型"""
    pass

class FileSizeError(ValidationError):
    """文件大小超出限制"""
    pass

class InvalidURL(ValidationError):
    """无效的 URL"""
    pass
```

#### 处理示例

```python
try:
    await processor.verify_and_process_image(file_path)
except InvalidFileType as e:
    logger.error(f"不支持的文件类型: {e}")
    # 建议: 提示用户支持的文件类型
except FileSizeError as e:
    logger.error(f"文件太大: {e}")
    # 建议: 提示用户文件大小限制
except InvalidURL as e:
    logger.error(f"无效的URL: {e}")
    # 建议: 检查URL格式是否正确
```

### 2. 处理错误

```python
class ProcessingError(Exception):
    """处理过程中的错误基类"""
    pass

class ImageProcessingError(ProcessingError):
    """图片处理错误"""
    pass

class MarkdownProcessingError(ProcessingError):
    """Markdown处理错误"""
    pass

class UploadError(ProcessingError):
    """上传错误"""
    pass
```

#### 处理示例

```python
try:
    await processor.process_image(file_path)
except ImageProcessingError as e:
    logger.error(f"图片处理失败: {e}")
    # 建议: 检查图片是否损坏
except MarkdownProcessingError as e:
    logger.error(f"Markdown处理失败: {e}")
    # 建议: 检查Markdown语法
except UploadError as e:
    logger.error(f"上传失败: {e}")
    # 建议: 检查网络连接和存储配置
```

### 3. 系统错误

```python
class SystemError(Exception):
    """系统相关错误的基类"""
    pass

class ResourceExhaustedError(SystemError):
    """系统资源不足"""
    pass

class ConfigurationError(SystemError):
    """配置错误"""
    pass
```

#### 处理示例

```python
try:
    await processor.process_batch(items)
except ResourceExhaustedError as e:
    logger.error(f"系统资源不足: {e}")
    # 建议: 减少并发数量或等待系统资源释放
except ConfigurationError as e:
    logger.error(f"配置错误: {e}")
    # 建议: 检查配置文件和环境变量
```

## 错误恢复策略

### 1. 自动重试

对于可恢复的错误（如网络超时），系统会自动重试：

```python
from mdimg_transfer.retry import RetryConfig, with_retry

retry_config = RetryConfig(
    max_retries=3,
    delay=1.0,
    backoff=2.0,
    exceptions=(ConnectionError, TimeoutError)
)

@with_retry(retry_config)
async def download_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()
```

### 2. 断点续传

对于大文件处理，支持断点续传：

```python
async def process_large_file(file_path: str):
    checkpoint_file = f"{file_path}.checkpoint"
    
    # 检查断点
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        # 从断点继续
        start_position = checkpoint['position']
    else:
        start_position = 0
    
    try:
        # 处理文件
        with open(file_path, 'rb') as f:
            f.seek(start_position)
            # 处理剩余内容...
            
    except Exception as e:
        # 保存断点
        with open(checkpoint_file, 'w') as f:
            json.dump({'position': current_position}, f)
        raise
```

### 3. 优雅降级

当遇到非致命错误时，系统会尝试使用替代方案：

```python
async def process_image(file_path: str):
    try:
        # 尝试最佳质量处理
        return await process_high_quality(file_path)
    except ResourceExhaustedError:
        logger.warning("资源不足，切换到低质量处理")
        return await process_low_quality(file_path)
    except Exception as e:
        logger.error(f"处理失败: {e}")
        return None
```

## 错误日志和监控

### 1. 日志记录

使用结构化日志记录错误信息：

```python
import logging
import json

logger = logging.getLogger(__name__)

def log_error(error_type: str, error: Exception, context: dict):
    """记录详细的错误信息"""
    error_info = {
        'type': error_type,
        'message': str(error),
        'timestamp': datetime.now().isoformat(),
        'context': context
    }
    logger.error(json.dumps(error_info))
```

### 2. 错误统计

收集错误统计信息：

```python
from collections import Counter
from datetime import datetime, timedelta

class ErrorTracker:
    def __init__(self):
        self.error_counts = Counter()
        self.error_timestamps = []
        
    def record_error(self, error_type: str):
        """记录错误"""
        self.error_counts[error_type] += 1
        self.error_timestamps.append(datetime.now())
        
    def get_error_rate(self, minutes: int = 5) -> float:
        """计算最近N分钟的错误率"""
        recent = datetime.now() - timedelta(minutes=minutes)
        recent_errors = [t for t in self.error_timestamps if t > recent]
        return len(recent_errors) / minutes
```

## 最佳实践

1. **始终使用类型注解**
   ```python
   from typing import Optional, Dict, Any
   
   def process_file(path: str) -> Optional[Dict[str, Any]]:
       pass
   ```

2. **使用上下文管理器**
   ```python
   async with ImageProcessor() as processor:
       await processor.process_image(file_path)
   ```

3. **提供详细的错误信息**
   ```python
   class ImageProcessingError(Exception):
       def __init__(self, message: str, file_path: str, details: dict):
           self.file_path = file_path
           self.details = details
           super().__init__(f"{message} - File: {file_path} - Details: {details}")
   ```

4. **实现清理机制**
   ```python
   def cleanup_temp_files(temp_dir: str):
       """清理临时文件"""
       for file in os.listdir(temp_dir):
           if file.endswith('.tmp'):
               try:
                   os.remove(os.path.join(temp_dir, file))
               except OSError as e:
                   logger.warning(f"清理临时文件失败: {e}")
   ```

5. **使用错误码**
   ```python
   from enum import Enum
   
   class ErrorCode(Enum):
       FILE_NOT_FOUND = "E001"
       INVALID_FORMAT = "E002"
       PROCESSING_FAILED = "E003"
       UPLOAD_FAILED = "E004"
   ```

6. **实现健康检查**
   ```python
   async def health_check() -> Dict[str, Any]:
       """系统健康检查"""
       return {
           'status': 'healthy',
           'error_rate': error_tracker.get_error_rate(),
           'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024,
           'cpu_usage': psutil.cpu_percent()
       }
   ```
