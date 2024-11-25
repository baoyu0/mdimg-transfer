# 安装和配置指南

本文档详细说明了 Markdown Image Transfer 工具的安装步骤、配置选项和使用方法。

## 1. 系统要求

- Python 3.7+
- 操作系统：Windows/Linux/macOS
- 内存：至少 2GB RAM
- 磁盘空间：至少 1GB 可用空间

## 2. 安装步骤

### 2.1 使用 pip 安装（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装包
pip install mdimg-transfer
```

### 2.2 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/mdimg-transfer.git
cd mdimg-transfer

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 3. 依赖项

### 3.1 必需依赖

```txt
# requirements.txt
pillow>=9.0.0
aiohttp>=3.8.0
boto3>=1.26.0
python-magic>=0.4.27
psutil>=5.9.0
aiofiles>=23.1.0
```

### 3.2 可选依赖

```txt
# requirements-optional.txt
redis>=4.5.0  # 用于缓存
pytest>=7.3.1  # 用于测试
black>=23.3.0  # 用于代码格式化
```

## 4. 配置

### 4.1 基本配置

创建配置文件 `config.yml`：

```yaml
# config.yml
processing:
  max_concurrent_tasks: 4
  max_retries: 3
  timeout: 30
  chunk_size: 8192

image:
  max_size: 1024
  quality: 85
  formats:
    - jpeg
    - png
    - webp
  optimize: true

storage:
  type: s3  # 或 local
  bucket: your-bucket-name
  region: your-region
  endpoint: your-endpoint-url

cache:
  enabled: true
  type: redis  # 或 memory
  ttl: 3600
  max_size: 1000

logging:
  level: INFO
  file: logs/app.log
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### 4.2 环境变量

设置必要的环境变量：

```bash
# AWS 配置
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
export ENDPOINT_URL=your_endpoint_url

# Redis 配置（可选）
export REDIS_URL=redis://localhost:6379

# 应用配置
export MAX_WORKERS=4
export LOG_LEVEL=INFO
```

## 5. 使用方法

### 5.1 命令行使用

```bash
# 处理单个文件
mdimg-transfer process path/to/your/file.md

# 处理目录
mdimg-transfer process path/to/your/directory

# 指定配置文件
mdimg-transfer process --config path/to/config.yml file.md

# 显示帮助
mdimg-transfer --help
```

### 5.2 Python API 使用

```python
from mdimg_transfer import ImageProcessor, Config

# 创建配置
config = Config.from_file('config.yml')

# 创建处理器
processor = ImageProcessor(config)

# 处理单个文件
await processor.process_file('path/to/file.md')

# 处理目录
await processor.process_directory('path/to/directory')
```

## 6. 验证安装

### 6.1 运行测试

```bash
# 安装测试依赖
pip install -r requirements-test.txt

# 运行测试
pytest tests/

# 运行特定测试
pytest tests/test_image_processor.py -v
```

### 6.2 检查安装

```python
# 验证安装
python -c "import mdimg_transfer; print(mdimg_transfer.__version__)"

# 检查依赖
pip freeze | grep mdimg-transfer
```

## 7. 常见问题

### 7.1 安装问题

1. **依赖冲突**
   ```bash
   # 解决方案
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

2. **权限问题**
   ```bash
   # Windows
   运行命令提示符为管理员

   # Linux/macOS
   sudo pip install mdimg-transfer
   ```

### 7.2 配置问题

1. **找不到配置文件**
   - 检查配置文件路径
   - 确保配置文件格式正确

2. **环境变量未生效**
   - 重新加载终端
   - 检查环境变量是否正确设置

## 8. 升级指南

### 8.1 使用 pip 升级

```bash
# 升级到最新版本
pip install --upgrade mdimg-transfer

# 升级到特定版本
pip install --upgrade mdimg-transfer==1.2.0
```

### 8.2 从源码升级

```bash
# 更新源码
git pull origin main

# 重新安装
pip install -e .
```

## 9. 卸载

```bash
# 使用 pip 卸载
pip uninstall mdimg-transfer

# 清理配置和缓存
rm -rf ~/.mdimg-transfer  # Linux/macOS
rd /s /q %USERPROFILE%\.mdimg-transfer  # Windows
```

## 10. 安全建议

1. **API 密钥管理**
   - 使用环境变量存储敏感信息
   - 定期轮换密钥
   - 避免在代码中硬编码密钥

2. **文件权限**
   - 设置适当的文件权限
   - 定期清理临时文件
   - 使用安全的临时目录

3. **网络安全**
   - 使用 HTTPS
   - 实现请求限流
   - 验证所有外部输入

## 11. 性能优化建议

1. **并发处理**
   - 根据系统配置调整并发数
   - 监控系统资源使用

2. **缓存配置**
   - 启用适当的缓存级别
   - 定期清理过期缓存

3. **内存管理**
   - 控制批处理大小
   - 及时释放资源

## 12. 故障排除清单

- [ ] 检查 Python 版本兼容性
- [ ] 验证所有必需依赖已安装
- [ ] 确认配置文件格式正确
- [ ] 检查环境变量设置
- [ ] 验证存储配置
- [ ] 检查网络连接
- [ ] 确认文件权限
- [ ] 验证缓存配置
