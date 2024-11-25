# Markdown Image Transfer API 文档

本文档详细说明了 Markdown Image Transfer 工具的 API 接口和使用方法。

## 1. 核心类

### 1.1 ImageProcessor

主要的图片处理类，负责图片的下载、处理和优化。

```python
class ImageProcessor:
    """图片处理器，负责图片的下载、处理和优化"""
    
    def __init__(self, config: Config = None):
        """
        初始化图片处理器
        
        Args:
            config (Config): 配置对象，如果为 None 则使用默认配置
        """
        self.config = config or Config()
        
    async def process_image(self, url: str, options: Dict = None) -> ProcessResult:
        """
        处理图片：下载、验证、优化
        
        Args:
            url (str): 图片URL
            options (Dict): 处理选项，可包含：
                - quality: 压缩质量 (1-100)
                - max_width: 最大宽度
                - max_height: 最大高度
                - format: 目标格式
                - strip_metadata: 是否清除元数据
                
        Returns:
            ProcessResult: 处理结果对象
        """
        pass
```

### 1.2 MarkdownProcessor

Markdown文件处理类，负责解析和更新Markdown文件。

```python
class MarkdownProcessor:
    """Markdown处理器，负责解析和更新Markdown文件"""
    
    async def process_file(self, file_path: str) -> ProcessResult:
        """
        处理Markdown文件
        
        Args:
            file_path (str): Markdown文件路径
            
        Returns:
            ProcessResult: 处理结果对象
        """
        pass
```

### 1.3 StorageManager

存储管理类，负责文件上传和管理。

```python
class StorageManager:
    """存储管理器，负责文件上传和管理"""
    
    async def upload_file(self, file_path: str, target_path: str) -> str:
        """
        上传文件到存储
        
        Args:
            file_path (str): 本地文件路径
            target_path (str): 目标路径
            
        Returns:
            str: 文件的公共访问URL
        """
        pass
```

## 2. 配置选项

### 2.1 图片处理配置

```python
class ImageConfig:
    """图片处理配置"""
    
    def __init__(self):
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.quality = 85
        self.max_width = 1920
        self.max_height = 1080
        self.strip_metadata = True
        self.progressive = True
        self.supported_formats = ['JPEG', 'PNG', 'GIF', 'WEBP', 'SVG']
```

### 2.2 存储配置

```python
class StorageConfig:
    """存储配置"""
    
    def __init__(self):
        self.endpoint_url = os.getenv('R2_ENDPOINT_URL')
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('R2_BUCKET_NAME')
        self.public_url = os.getenv('R2_PUBLIC_URL')
```

## 3. 特殊功能

### 3.1 SVG处理

```python
class SVGProcessor:
    """SVG处理器"""
    
    @staticmethod
    def is_svg_content(content: str) -> bool:
        """
        检查内容是否是SVG
        
        Args:
            content (str): 要检查的内容
            
        Returns:
            bool: 是否是SVG内容
        """
        pass
        
    @staticmethod
    def is_placeholder_svg(content: str) -> bool:
        """
        检查是否是占位SVG
        
        Args:
            content (str): SVG内容
            
        Returns:
            bool: 是否是占位图片
        """
        pass
```

### 3.2 WeChat图片处理

```python
class WeChatImageProcessor:
    """微信图片处理器"""
    
    async def process_wechat_url(self, url: str) -> str:
        """
        处理微信图片URL
        
        Args:
            url (str): 原始URL
            
        Returns:
            str: 处理后的URL
        """
        pass
```

## 4. 错误处理

### 4.1 异常类

```python
class ImageProcessError(Exception):
    """图片处理错误"""
    pass

class DownloadError(Exception):
    """下载错误"""
    pass

class ValidationError(Exception):
    """验证错误"""
    pass
```

### 4.2 错误恢复

```python
class RetryManager:
    """重试管理器"""
    
    async def retry_with_timeout(self, func, *args, **kwargs):
        """
        带超时的重试机制
        
        Args:
            func: 要重试的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            Any: 函数返回值
        """
        pass
```

## 5. 工具函数

### 5.1 URL处理

```python
def process_url(url: str) -> str:
    """处理URL，规范化并验证"""
    pass

def get_file_extension(url: str) -> str:
    """从URL获取文件扩展名"""
    pass
```

### 5.2 文件处理

```python
def create_temp_file() -> str:
    """创建临时文件"""
    pass

def clean_temp_files():
    """清理临时文件"""
    pass
```

## 6. 使用示例

### 6.1 基本使用

```python
from mdimg_transfer import ImageProcessor, MarkdownProcessor

async def process_markdown_file(file_path: str):
    # 初始化处理器
    image_processor = ImageProcessor()
    markdown_processor = MarkdownProcessor()
    
    # 处理文件
    result = await markdown_processor.process_file(file_path)
    
    # 检查结果
    if result.success:
        print(f"处理完成: {result.output_path}")
    else:
        print(f"处理失败: {result.error}")
```

### 6.2 自定义配置

```python
from mdimg_transfer import ImageConfig, StorageConfig

# 创建自定义配置
image_config = ImageConfig()
image_config.quality = 90
image_config.max_width = 2560
image_config.strip_metadata = True

# 使用自定义配置
processor = ImageProcessor(config=image_config)
```

### 6.3 错误处理

```python
from mdimg_transfer import ImageProcessError

try:
    result = await processor.process_image(url)
except ImageProcessError as e:
    print(f"处理错误: {e}")
except DownloadError as e:
    print(f"下载错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 7. 最佳实践

1. 总是使用异步操作以获得最佳性能
2. 适当配置重试机制和超时
3. 使用临时文件处理大文件
4. 正确处理异常和清理资源
5. 使用日志记录重要操作和错误

## 8. 注意事项

1. 图片大小限制：50MB
2. 支持的图片格式：JPEG, PNG, GIF, WEBP, SVG
3. 默认图片质量：85%
4. 最大图片尺寸：1920x1080
5. 自动清除元数据
6. 使用渐进式JPEG
7. SVG文件特殊处理
