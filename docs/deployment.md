# 部署指南

本文档提供了 Markdown Image Transfer 工具的详细部署说明。

## 1. 系统要求

### 1.1 硬件要求
- CPU: 2核心及以上
- 内存: 4GB及以上
- 磁盘空间: 20GB及以上

### 1.2 软件要求
- Python 3.10+
- pip 21.0+
- Git
- 可选: Docker 20.10+

## 2. 安装步骤

### 2.1 从源码安装

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/mdimg-transfer.git
cd mdimg-transfer

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -e .
```

### 2.2 使用 Docker 安装

```bash
# 1. 构建镜像
docker build -t mdimg-transfer .

# 2. 运行容器
docker run -d \
    -p 8000:8000 \
    -v /path/to/data:/app/data \
    --name mdimg-transfer \
    mdimg-transfer
```

## 3. 配置

### 3.1 环境变量
复制 `.env.example` 到 `.env` 并配置以下环境变量：

```bash
# 基础配置
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secret-key

# 存储配置
STORAGE_TYPE=s3  # 可选: local, s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=your-region
S3_BUCKET=your-bucket

# 缓存配置
REDIS_URL=redis://localhost:6379/0

# 性能配置
MAX_WORKERS=4
BATCH_SIZE=100
```

### 3.2 应用配置
在 `config.py` 中可以配置更多高级选项：

```python
# 图片处理配置
IMAGE_MAX_SIZE = 1920
IMAGE_QUALITY = 85
ALLOWED_FORMATS = ['jpg', 'png', 'webp']

# 缓存配置
CACHE_TTL = 3600
MAX_CACHE_SIZE = 1000

# 并发配置
MAX_CONCURRENT_TASKS = 10
TASK_TIMEOUT = 300
```

## 4. 运行

### 4.1 开发环境

```bash
# 使用 hypercorn 运行
hypercorn app:app --reload --bind 0.0.0.0:8000
```

### 4.2 生产环境

推荐使用 systemd 管理服务：

```ini
# /etc/systemd/system/mdimg-transfer.service
[Unit]
Description=Markdown Image Transfer Service
After=network.target

[Service]
User=mdimg
Group=mdimg
WorkingDirectory=/opt/mdimg-transfer
Environment="PATH=/opt/mdimg-transfer/venv/bin"
ExecStart=/opt/mdimg-transfer/venv/bin/hypercorn app:app --bind 0.0.0.0:8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl start mdimg-transfer
sudo systemctl enable mdimg-transfer
```

## 5. 监控

### 5.1 日志
日志文件位于 `logs/app.log`，使用 ELK 或其他日志管理工具收集和分析。

### 5.2 指标监控
应用暴露了 Prometheus 指标端点：`/metrics`

主要指标：
- `mdimg_requests_total`: 请求总数
- `mdimg_request_duration_seconds`: 请求处理时间
- `mdimg_image_size_bytes`: 图片大小分布
- `mdimg_processing_errors_total`: 处理错误数

### 5.3 健康检查
健康检查端点：`/health`

## 6. 备份

### 6.1 数据备份
定期备份以下数据：
- 数据库文件
- 配置文件
- 上传的图片

示例备份脚本：

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d)

# 备份数据库
sqlite3 data/app.db ".backup $BACKUP_DIR/db_$DATE.sqlite"

# 备份配置
cp .env $BACKUP_DIR/env_$DATE
cp config.py $BACKUP_DIR/config_$DATE

# 备份图片
tar -czf $BACKUP_DIR/images_$DATE.tar.gz data/images/

# 保留最近30天的备份
find $BACKUP_DIR -type f -mtime +30 -delete
```

## 7. 安全

### 7.1 系统安全
- 使用最小权限原则
- 定期更新系统和依赖
- 启用防火墙
- 使用 HTTPS

### 7.2 应用安全
- 设置强密码和密钥
- 限制上传文件大小和类型
- 启用请求速率限制
- 配置 CORS

## 8. 故障排除

### 8.1 常见问题

1. 启动失败
   - 检查端口占用
   - 检查环境变量
   - 检查日志文件

2. 图片处理失败
   - 检查存储权限
   - 检查磁盘空间
   - 检查内存使用

3. 性能问题
   - 调整工作进程数
   - 优化图片处理参数
   - 检查缓存配置

### 8.2 日志分析

使用以下命令分析日志：

```bash
# 查看错误日志
grep ERROR logs/app.log

# 查看慢请求
grep "took longer than" logs/app.log

# 统计请求量
grep "Request completed" logs/app.log | wc -l
```

## 9. 升级

### 9.1 升级步骤

1. 备份数据
```bash
./scripts/backup.sh
```

2. 更新代码
```bash
git pull origin main
```

3. 更新依赖
```bash
pip install -e .
```

4. 迁移数据库
```bash
python scripts/migrate.py
```

5. 重启服务
```bash
sudo systemctl restart mdimg-transfer
```

### 9.2 回滚步骤

如果升级失败：

1. 停止服务
```bash
sudo systemctl stop mdimg-transfer
```

2. 还原代码
```bash
git checkout previous-version
```

3. 还原数据
```bash
./scripts/restore.sh
```

4. 重启服务
```bash
sudo systemctl start mdimg-transfer
```

## 10. 性能调优

### 10.1 应用调优

1. 工作进程数
```python
workers = min(cpu_count() * 2 + 1, 8)
```

2. 内存限制
```python
MAX_MEMORY_PERCENT = 80
```

3. 缓存配置
```python
CACHE_STRATEGY = 'lru'
CACHE_SIZE = 1000
```

### 10.2 系统调优

1. 文件描述符限制
```bash
# /etc/security/limits.conf
mdimg soft nofile 65535
mdimg hard nofile 65535
```

2. TCP 调优
```bash
# /etc/sysctl.conf
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
```

## 11. 维护

### 11.1 定期维护任务

1. 日志轮转
```bash
# /etc/logrotate.d/mdimg-transfer
/opt/mdimg-transfer/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 mdimg mdimg
    sharedscripts
    postrotate
        systemctl reload mdimg-transfer
    endscript
}
```

2. 清理临时文件
```bash
find /tmp -name "mdimg-*" -mtime +1 -delete
```

3. 数据库优化
```bash
sqlite3 data/app.db "VACUUM;"
```

### 11.2 监控检查

1. 磁盘使用
```bash
df -h /opt/mdimg-transfer
```

2. 内存使用
```bash
free -m
```

3. 进程状态
```bash
systemctl status mdimg-transfer
```

## 12. 支持

### 12.1 获取帮助

- GitHub Issues: https://github.com/yourusername/mdimg-transfer/issues
- 文档: https://mdimg-transfer.readthedocs.io/
- 邮件: support@mdimg-transfer.com

### 12.2 报告问题

报告问题时请提供：

1. 系统信息
```bash
python --version
pip freeze
uname -a
```

2. 错误日志
```bash
tail -n 100 logs/app.log
```

3. 配置信息（注意删除敏感信息）
```bash
cat config.py
```
