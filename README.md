# MDImg Transfer

一个强大的 Web 应用程序，用于处理和转换 Markdown 文件和网页中的图片链接。支持将图片迁移到 Cloudflare R2 存储，并自动更新文档中的图片链接。

## 项目目标

本项目旨在解决两个主要场景：

1. **Markdown文件处理**：上传Markdown文件后，自动下载文件中的图片并上传至R2存储，然后更新文件中的图片链接，最后提供处理后的文件下载。

2. **网页内容转换**：输入网页URL后，自动将网页内容转换为Markdown格式，同时处理其中的图片（下载并上传至R2），最后提供包含新图片链接的Markdown文件下载。

## 主要功能

### Markdown 文件处理
- 支持拖放上传 Markdown 文件
- 自动下载文件中的图片
- 上传图片到 Cloudflare R2 存储
- 更新文件中的图片链接
- 下载处理后的 Markdown 文件
- WebSocket 实时进度显示

### 网页转换
- 输入网页 URL 自动抓取内容
- 将网页内容转换为 Markdown 格式
- 自动处理网页中的图片
- 生成包含新图片链接的 Markdown 文件
- 实时转换进度反馈

### 用户界面特性
- 简洁现代的界面设计
- 深色/浅色主题切换（支持跟随系统）
- 实时处理进度显示
- 友好的状态反馈提示
- 响应式布局设计
- Tab 式任务切换

## 快速开始

### 环境要求
- Python 3.10 或更高版本
- pip 包管理器
- Node.js（用于Tailwind CSS构建）

### 1. 克隆项目
```bash
# 使用 SSH 克隆（推荐）
git clone git@github.com:baoyu0/mdimg-transfer.git
cd mdimg-transfer

# 切换到开发分支
git checkout dev
```

### 2. 配置环境变量
创建 `.env` 文件并配置以下参数：
```env
# 服务器配置
PORT=5000
DEBUG=True

# R2 存储配置
R2_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://pub-xxx.r2.dev

# 日志配置
LOG_LEVEL=DEBUG
```

### 3. 安装依赖
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Node.js 依赖
npm install
```

### 4. 构建前端资源
```bash
# 构建 Tailwind CSS
npm run build

# 监听模式（开发时使用）
npm run watch
```

### 5. 服务器管理
使用 `server_control.py` 来管理服务器：

```bash
# 启动服务器
python server_control.py start

# 停止服务器
python server_control.py stop

# 重启服务器
python server_control.py restart
```

服务器将在配置的端口上启动（默认 http://localhost:5000）

## 开发指南

### 项目结构
```
mdimg-transfer/
├── mdimg_transfer/        # 主应用程序包
│   ├── services/         # 服务层
│   ├── utils/           # 工具函数
│   └── app.py           # 应用程序入口
├── static/              # 静态资源
│   ├── css/            # 样式文件
│   └── js/             # JavaScript 文件
├── templates/           # HTML 模板
├── logs/               # 日志文件
├── uploads/            # 上传文件临时目录
├── processed/          # 处理后的文件
└── images/             # 下载的图片缓存
```

### 开发流程
1. 确保在 dev 分支上进行开发：
   ```bash
   git checkout dev
   git pull
   ```

2. 创建功能分支（可选）：
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. 启动开发环境：
   ```bash
   # 终端 1：启动 Tailwind CSS 监听
   npm run watch

   # 终端 2：启动服务器（自动重载模式）
   python server_control.py start
   ```

### 调试提示
- 检查 `logs` 目录下的日志文件以获取详细信息
- 使用浏览器开发者工具查看 WebSocket 连接状态
- 服务器问题优先使用 `server_control.py stop` 清理进程

## 技术栈

### 后端
- Quart: 异步 Python Web 框架
- Hypercorn: ASGI 服务器
- aiohttp: 异步 HTTP 客户端
- boto3: AWS/R2 SDK
- python-dotenv: 环境变量管理
- psutil: 进程管理

### 前端
- Vanilla JavaScript
- Tailwind CSS
- SweetAlert2
- WebSocket API

## 许可证

本项目采用 MIT 许可证
