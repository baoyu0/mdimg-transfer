# 开发者指南

本文档提供了 Markdown Image Transfer 工具的开发指南和最佳实践。

## 1. 开发环境设置

### 1.1 开发工具

推荐使用以下工具：

- IDE: VS Code 或 PyCharm
- Python 版本管理: pyenv
- 依赖管理: poetry
- 代码格式化: black
- 代码检查: flake8, mypy
- 测试框架: pytest
- 文档生成: Sphinx

### 1.2 开发环境配置

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/mdimg-transfer.git
cd mdimg-transfer

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 3. 安装开发依赖
pip install -r requirements-dev.txt
```

## 2. 代码规范

### 2.1 Python 代码风格

遵循 PEP 8 规范，并使用 black 进行格式化：

```python
# 正确的导入顺序
import os
import sys
from typing import Dict, List, Optional

import aiohttp
import PIL
from fastapi import FastAPI

from mdimg_transfer.core import ImageProcessor
from mdimg_transfer.utils import normalize_url

# 正确的类定义
class ImageHandler:
    """图片处理器类"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._initialize()

    def process_image(self, image_path: str) -> Optional[str]:
        """
        处理图片

        Args:
            image_path: 图片路径

        Returns:
            处理后的图片路径，失败返回 None
        """
        try:
            return self._process(image_path)
        except Exception as e:
            logger.error(f"处理失败: {e}")
            return None

    def _initialize(self) -> None:
        """初始化处理器"""
        pass

    def _process(self, path: str) -> str:
        """内部处理方法"""
        pass
```

### 2.2 文档规范

使用 Google 风格的文档字符串：

```python
def process_markdown(
    content: str,
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    处理 Markdown 内容中的图片

    Args:
        content: Markdown 内容
        options: 处理选项
            - max_size (int): 最大图片尺寸
            - quality (int): 压缩质量
            - format (str): 输出格式

    Returns:
        处理后的 Markdown 内容

    Raises:
        ValueError: 内容为空
        ProcessingError: 处理失败

    Example:
        >>> content = "![image](http://example.com/image.jpg)"
        >>> process_markdown(content, {"max_size": 800})
        '![image](http://example.com/image_800.jpg)'
    """
    pass
```

### 2.3 类型注解

使用类型注解并用 mypy 检查：

```python
from typing import (
    Dict, List, Optional, Union,
    TypeVar, Generic, Callable
)

T = TypeVar('T')

class Result(Generic[T]):
    """通用结果类"""

    def __init__(
        self,
        value: Optional[T] = None,
        error: Optional[Exception] = None
    ) -> None:
        self.value = value
        self.error = error

    @property
    def is_success(self) -> bool:
        return self.error is None

class Cache(Generic[T]):
    """通用缓存类"""

    def __init__(self) -> None:
        self._data: Dict[str, T] = {}

    def get(self, key: str) -> Optional[T]:
        return self._data.get(key)

    def set(self, key: str, value: T) -> None:
        self._data[key] = value
```

## 3. 项目结构

```
mdimg_transfer/
├── docs/                    # 文档
│   ├── api/                # API 文档
│   ├── guides/             # 用户指南
│   └── examples/           # 示例
├── src/                    # 源代码
│   └── mdimg_transfer/
│       ├── __init__.py
│       ├── core/           # 核心功能
│       │   ├── __init__.py
│       │   ├── processor.py
│       │   └── storage.py
│       ├── utils/          # 工具函数
│       └── cli/            # 命令行接口
├── tests/                  # 测试
│   ├── __init__.py
│   ├── unit/              # 单元测试
│   └── integration/       # 集成测试
├── examples/               # 示例代码
├── scripts/                # 工具脚本
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── setup.py
└── README.md
```

## 4. 测试规范

### 4.1 单元测试

```python
import pytest
from mdimg_transfer.core import ImageProcessor

def test_image_processor_init():
    """测试初始化"""
    processor = ImageProcessor()
    assert processor is not None
    assert processor.config is not None

@pytest.mark.asyncio
async def test_process_image():
    """测试图片处理"""
    processor = ImageProcessor()
    result = await processor.process_image(
        "test.jpg",
        max_size=800
    )
    assert result is not None
    assert result['size'] < 1024 * 1024
    assert result['dimensions'][0] <= 800

@pytest.mark.parametrize("url,expected", [
    ("http://example.com/image.jpg", True),
    ("invalid_url", False),
])
def test_url_validation(url: str, expected: bool):
    """测试 URL 验证"""
    assert ImageProcessor.is_valid_url(url) == expected
```

### 4.2 集成测试

```python
import pytest
from mdimg_transfer import create_app
from mdimg_transfer.core import Config

@pytest.fixture
async def app():
    """创建测试应用"""
    config = Config.from_dict({
        'testing': True,
        'storage': {
            'type': 'memory'
        }
    })
    app = create_app(config)
    yield app

async def test_upload_endpoint(app):
    """测试上传端点"""
    client = app.test_client()
    response = await client.post(
        '/upload',
        data={'file': open('test.jpg', 'rb')}
    )
    assert response.status_code == 200
    assert 'url' in response.json
```

## 5. 版本控制

### 5.1 Git 提交规范

使用语义化的提交消息：

```bash
# 功能开发
git commit -m "feat: 添加图片压缩功能"

# 修复 bug
git commit -m "fix: 修复大文件处理内存泄漏"

# 文档更新
git commit -m "docs: 更新 API 文档"

# 性能优化
git commit -m "perf: 优化图片处理性能"

# 重构代码
git commit -m "refactor: 重构存储模块"
```

### 5.2 版本号规范

使用语义化版本号：

- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

## 6. CI/CD 配置

### 6.1 GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Check code style
      run: |
        black --check .
        flake8 .
        mypy src/
```

## 7. 性能优化

### 7.1 代码优化

```python
from functools import lru_cache
import asyncio
from typing import List

class ImageProcessor:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()
    
    @lru_cache(maxsize=1000)
    def _get_image_info(self, url: str) -> dict:
        """缓存图片信息"""
        pass
    
    async def process_batch(self, urls: List[str]) -> List[dict]:
        """并行处理多个图片"""
        async with self._lock:
            tasks = [self.process_image(url) for url in urls]
            return await asyncio.gather(*tasks)
```

### 7.2 内存优化

```python
class ResourceManager:
    def __init__(self):
        self._resources = weakref.WeakSet()
    
    def register(self, resource):
        """注册资源"""
        self._resources.add(resource)
    
    def cleanup(self):
        """清理资源"""
        for resource in self._resources:
            try:
                resource.close()
            except Exception as e:
                logger.warning(f"清理失败: {e}")
```

## 8. 安全最佳实践

### 8.1 输入验证

```python
from typing import Optional
from pydantic import BaseModel, HttpUrl

class ImageRequest(BaseModel):
    """图片处理请求模型"""
    url: HttpUrl
    max_size: Optional[int] = 1024
    quality: Optional[int] = 85
    
    @validator('quality')
    def validate_quality(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('质量必须在 0-100 之间')
        return v
```

### 8.2 安全处理

```python
import secrets
import hashlib
from pathlib import Path

def secure_filename(filename: str) -> str:
    """生成安全的文件名"""
    name = Path(filename).stem
    ext = Path(filename).suffix
    return f"{hashlib.sha256(name.encode()).hexdigest()[:8]}{ext}"

def generate_token() -> str:
    """生成安全的令牌"""
    return secrets.token_urlsafe(32)
```

## 9. 错误处理

### 9.1 自定义异常

```python
class MDImageError(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(MDImageError):
    """验证错误"""
    pass

class ProcessingError(MDImageError):
    """处理错误"""
    pass
```

### 9.2 错误处理装饰器

```python
from functools import wraps
from typing import Type

def handle_errors(*error_types: Type[Exception]):
    """错误处理装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except error_types as e:
                logger.error(f"操作失败: {e}")
                return None
        return wrapper
    return decorator
```

## 10. 文档生成

### 10.1 Sphinx 配置

```python
# docs/conf.py
project = 'MDImage Transfer'
copyright = '2023, Your Name'
author = 'Your Name'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'
```

### 10.2 API 文档生成

```bash
# 生成 API 文档
sphinx-apidoc -f -o docs/api src/mdimg_transfer

# 构建文档
cd docs
make html
```

## 11. 发布流程

### 11.1 发布检查清单

- [ ] 更新版本号
- [ ] 更新更新日志
- [ ] 运行测试套件
- [ ] 检查文档
- [ ] 构建分发包
- [ ] 上传到 PyPI

### 11.2 发布脚本

```bash
#!/bin/bash
# scripts/release.sh

# 1. 更新版本号
poetry version patch

# 2. 运行测试
pytest tests/

# 3. 构建包
poetry build

# 4. 发布到 PyPI
poetry publish
```

## 12. 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 运行测试
5. 提交 Pull Request

### 12.1 Pull Request 模板

```markdown
## 描述
简要描述你的更改

## 类型
- [ ] 功能新增
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 性能优化
- [ ] 其他

## 测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] 手动测试

## 检查清单
- [ ] 代码符合规范
- [ ] 添加测试
- [ ] 更新文档
- [ ] 更新更新日志
```
