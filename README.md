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

### 网页转换
- 输入网页 URL 自动抓取内容
- 将网页内容转换为 Markdown 格式
- 自动处理网页中的图片
- 生成包含新图片链接的 Markdown 文件

### 用户界面特性
- 简洁现代的界面设计
- 深色/浅色主题切换（支持跟随系统）
- 实时处理进度显示
- 友好的状态反馈提示

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
R2_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://pub-xxx.r2.dev
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
```

### 5. 启动服务器
```bash
python start_server.py
```

服务器将在 http://localhost:5000 启动

## 开发指南

### 分支策略
- `main`: 主分支，只接受来自 dev 分支的合并请求
- `dev`: 开发分支，所有开发工作在此分支进行
- 功能分支：从 dev 分支创建，完成后合并回 dev

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

3. 提交更改：
   ```bash
   git add .
   git commit -m "feat: your changes"
   git push
   ```

4. 合并到主分支：
   - 通过 GitHub 创建 Pull Request 从 dev 合并到 main
   - 等待代码审查
   - 合并后删除功能分支

### 代码风格
- Python: 遵循 PEP 8 规范
- JavaScript: 使用 ES6+ 特性
- HTML/CSS: 使用 Tailwind CSS 工具类

## 技术栈

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

## 项目结构

```
mdimg-transfer/
├── static/               # 静态资源
│   ├── css/             # 样式文件
│   │   └── output.css   # 编译后的 Tailwind CSS
│   └── js/              # JavaScript 文件
│       └── main.js      # 主要的前端逻辑
├── templates/           # HTML 模板
│   └── index.html      # 主页面模板
├── mdimg_transfer/     # 后端 Python 包
│   ├── core/          # 核心功能模块
│   ├── routes/        # API 路由
│   └── errors/        # 错误处理
├── start_server.py     # 服务器启动脚本
├── requirements.txt    # Python 依赖
├── package.json       # Node.js 依赖
└── .env              # 环境变量配置
```

## 贡献

欢迎提交 Issues 和 Pull Requests 来帮助改进项目。请确保：
1. Pull Request 提交到 dev 分支
2. 提交信息遵循约定式提交规范
3. 更新相关文档
4. 添加必要的测试

## 许可证

本项目采用 MIT 许可证。
