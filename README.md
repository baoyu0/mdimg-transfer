# MDImg Transfer

一个强大的 Web 应用程序，用于处理和转换 Markdown 文件和网页中的图片链接。支持将图片迁移到 Cloudflare R2 存储，并自动更新文档中的图片链接。

## 🎯 项目目标

本项目旨在解决两个主要场景：

1. **Markdown文件处理**：上传Markdown文件后，自动下载文件中的图片并上传至R2存储，然后更新文件中的图片链接，最后提供处理后的文件下载。

2. **网页内容转换**：输入网页URL后，自动将网页内容转换为Markdown格式，同时处理其中的图片（下载并上传至R2），最后提供包含新图片链接的Markdown文件下载。

## 🌟 主要功能

### Markdown 文件处理
- ✨ 支持拖放上传 Markdown 文件
- 📥 自动下载文件中的图片
- ☁️ 上传图片到 Cloudflare R2 存储
- 🔄 更新文件中的图片链接
- 📤 下载处理后的 Markdown 文件

### 网页转换
- 🌐 输入网页 URL 自动抓取内容
- 📝 将网页内容转换为 Markdown 格式
- 🖼️ 自动处理网页中的图片
- 📎 生成包含新图片链接的 Markdown 文件

### 用户界面特性
- 🎨 简洁现代的界面设计
- 🌓 深色/浅色主题切换
- 📊 实时处理进度显示
- 💬 友好的状态反馈提示

## 🚀 快速开始

### 环境要求
- Python 3.10 或更高版本
- pip 包管理器

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/mdimg-transfer.git
cd mdimg-transfer
```

### 2. 配置环境变量
创建 `.env` 文件并配置以下参数：
```env
R2_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://pub-xxx.r2.dev
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动服务器
```bash
python start_server.py
```

服务器将在 http://localhost:5000 启动

## 💻 使用说明

### 处理 Markdown 文件
1. 访问 http://localhost:5000
2. 点击"上传 Markdown 文件"按钮
3. 拖放或选择 Markdown 文件
4. 等待处理完成后自动下载结果文件

### 处理网页内容
1. 访问 http://localhost:5000
2. 点击"输入网页 URL"按钮
3. 输入要处理的网页地址
4. 点击"转换"按钮
5. 等待处理完成后自动下载结果文件

## 🔧 技术栈

### 后端
- Python 3.10
- Quart (异步 Web 框架)
- Hypercorn (ASGI 服务器)
- python-dotenv (环境变量管理)
- boto3 (AWS S3/R2 SDK)

### 前端
- 原生 JavaScript
- Tailwind CSS
- SweetAlert2 (通知提示)

### 存储
- Cloudflare R2 (兼容 S3 API)

## 📦 项目结构

```
mdimg-transfer/
├── static/               # 静态资源
│   ├── css/             # 样式文件
│   │   └── output.css   # 编译后的 Tailwind CSS
│   └── js/              # JavaScript 文件
│       └── main.js      # 主要的前端逻辑
├── templates/           # HTML 模板
│   └── index.html      # 主页面模板
├── start_server.py     # 服务器启动脚本
├── requirements.txt    # 项目依赖
└── .env               # 环境变量配置
```

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests 来帮助改进项目。

## 📄 许可证

本项目采用 MIT 许可证。
