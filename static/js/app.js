// WebSocket连接管理
class WebSocketManager {
    constructor() {
        this.clientId = Math.random().toString(36).substr(2, 9);
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.clientId}`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket连接已建立');
            this.reconnectAttempts = 0;
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket连接已关闭');
            this.reconnect();
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket错误:', error);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
    }

    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('WebSocket重连次数超过最大限制');
            return;
        }

        setTimeout(() => {
            this.reconnectAttempts++;
            this.connect();
        }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
    }

    handleMessage(data) {
        switch (data.type) {
            case 'progress':
                this.updateProgress(data);
                break;
            case 'result':
                this.handleResult(data);
                break;
            default:
                console.log('未知消息类型:', data);
        }
    }

    updateProgress(data) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const percentage = (data.current / data.total) * 100;
        
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = `处理进度: ${data.current}/${data.total}`;
        
        if (data.current === data.total) {
            document.getElementById('statusIndicator').className = 'status-indicator success';
            document.getElementById('statusText').textContent = '处理完成';
        }
    }

    handleResult(data) {
        const result = data.result;
        const resultsContainer = document.getElementById('results');
        
        const resultElement = document.createElement('div');
        resultElement.className = `file-info ${result.status === 'success' ? 'success' : 'error'}`;
        resultElement.innerHTML = `
            <div class="file-info-details">
                <div class="file-info-name">${result.filename}</div>
                <div class="file-info-status">${result.status === 'success' ? '处理成功' : '处理失败'}</div>
                ${result.error ? `<div class="file-info-error">${result.error}</div>` : ''}
            </div>
        `;
        
        resultsContainer.appendChild(resultElement);
    }

    sendMessage(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}

// 图片预览管理
class ImagePreview {
    constructor() {
        this.modal = null;
        this.currentImage = null;
        this.scale = 1;
        this.rotation = 0;
        this.setupPreviewModal();
    }

    setupPreviewModal() {
        // 创建预览模态窗口
        this.modal = document.createElement('div');
        this.modal.className = 'preview-modal';
        this.modal.innerHTML = `
            <div class="preview-container zoom-in">
                <div class="preview-header">
                    <div class="preview-title">图片预览</div>
                    <div class="preview-close">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </div>
                </div>
                <div class="preview-content">
                    <div class="preview-image-container">
                        <img class="preview-image" src="" alt="预览图片">
                    </div>
                    <div class="preview-info">
                        <div class="preview-info-item">
                            <span class="preview-info-label">文件名</span>
                            <span class="preview-info-value filename">-</span>
                        </div>
                        <div class="preview-info-item">
                            <span class="preview-info-label">大小</span>
                            <span class="preview-info-value filesize">-</span>
                        </div>
                        <div class="preview-info-item">
                            <span class="preview-info-label">类型</span>
                            <span class="preview-info-value filetype">-</span>
                        </div>
                        <div class="preview-info-item">
                            <span class="preview-info-label">尺寸</span>
                            <span class="preview-info-value dimensions">-</span>
                        </div>
                    </div>
                </div>
                <div class="preview-toolbar">
                    <button class="preview-tool-button zoom-in-btn">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
                        </svg>
                        放大
                    </button>
                    <button class="preview-tool-button zoom-out-btn">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7"></path>
                        </svg>
                        缩小
                    </button>
                    <button class="preview-tool-button rotate-btn">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                        </svg>
                        旋转
                    </button>
                    <button class="preview-tool-button reset-btn">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                        </svg>
                        重置
                    </button>
                </div>
            </div>
        `;

        // 添加事件监听
        this.modal.querySelector('.preview-close').addEventListener('click', () => this.close());
        this.modal.querySelector('.zoom-in-btn').addEventListener('click', () => this.zoomIn());
        this.modal.querySelector('.zoom-out-btn').addEventListener('click', () => this.zoomOut());
        this.modal.querySelector('.rotate-btn').addEventListener('click', () => this.rotate());
        this.modal.querySelector('.reset-btn').addEventListener('click', () => this.reset());

        // 添加键盘事件监听
        document.addEventListener('keydown', (e) => {
            if (this.modal.classList.contains('active')) {
                switch (e.key) {
                    case 'Escape':
                        this.close();
                        break;
                    case '+':
                        this.zoomIn();
                        break;
                    case '-':
                        this.zoomOut();
                        break;
                    case 'r':
                        this.rotate();
                        break;
                }
            }
        });

        document.body.appendChild(this.modal);
    }

    show(file) {
        this.currentImage = file;
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const img = this.modal.querySelector('.preview-image');
            img.src = e.target.result;
            
            // 更新图片信息
            this.updateImageInfo(file);
            
            // 重置缩放和旋转
            this.reset();
            
            // 显示模态窗口
            this.modal.classList.add('active');
            this.modal.querySelector('.preview-container').classList.add('zoom-in');
        };
        
        reader.readAsDataURL(file);
    }

    updateImageInfo(file) {
        const img = new Image();
        img.onload = () => {
            this.modal.querySelector('.filename').textContent = file.name;
            this.modal.querySelector('.filesize').textContent = this.formatFileSize(file.size);
            this.modal.querySelector('.filetype').textContent = file.type || '未知';
            this.modal.querySelector('.dimensions').textContent = `${img.width} × ${img.height}`;
        };
        img.src = URL.createObjectURL(file);
    }

    close() {
        this.modal.classList.remove('active');
        this.modal.querySelector('.preview-container').classList.remove('zoom-in');
        this.currentImage = null;
    }

    zoomIn() {
        this.scale = Math.min(this.scale + 0.1, 3);
        this.updateTransform();
    }

    zoomOut() {
        this.scale = Math.max(this.scale - 0.1, 0.1);
        this.updateTransform();
    }

    rotate() {
        this.rotation += 90;
        if (this.rotation >= 360) {
            this.rotation = 0;
        }
        this.updateTransform();
    }

    reset() {
        this.scale = 1;
        this.rotation = 0;
        this.updateTransform();
    }

    updateTransform() {
        const img = this.modal.querySelector('.preview-image');
        img.style.transform = `scale(${this.scale}) rotate(${this.rotation}deg)`;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// 文件处理管理
class FileProcessor {
    constructor(wsManager) {
        this.wsManager = wsManager;
        this.imagePreview = new ImagePreview();
        this.setupEventListeners();
        this.files = new Map(); // 存储文件引用
    }

    setupEventListeners() {
        const dragArea = document.getElementById('dragArea');
        const fileInput = document.getElementById('fileInput');
        const processBtn = document.getElementById('processBtn');

        // 拖放事件处理
        dragArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dragArea.classList.add('drag-over');
        });

        dragArea.addEventListener('dragleave', () => {
            dragArea.classList.remove('drag-over');
        });

        dragArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dragArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });

        // 文件输入事件处理
        fileInput.addEventListener('change', (e) => {
            const files = e.target.files;
            this.handleFiles(files);
        });

        // 处理按钮点击事件
        processBtn.addEventListener('click', () => {
            this.processFiles();
        });

        // 文件列表点击事件
        const fileList = document.getElementById('fileList');
        fileList.addEventListener('click', (e) => {
            const fileItem = e.target.closest('.file-info');
            if (!fileItem) return;

            const fileName = fileItem.querySelector('.file-info-name').textContent;
            const file = this.files.get(fileName);
            
            if (file) {
                // 检查是否点击了预览按钮
                if (e.target.closest('.preview-btn')) {
                    e.stopPropagation(); // 阻止事件冒泡
                    this.previewFile(file);
                } else {
                    // 点击整个文件项
                    this.previewFile(file);
                }
            }
        });
    }

    handleFiles(files) {
        // 清除旧的文件引用
        this.files.clear();

        const validFiles = Array.from(files).filter(file => {
            const isMarkdown = file.name.endsWith('.md') || file.name.endsWith('.markdown');
            const isImage = file.type.startsWith('image/');
            return isMarkdown || isImage;
        });

        if (validFiles.length === 0) {
            this.showError('请选择有效的Markdown文件或图片文件');
            return;
        }

        // 存储文件引用
        validFiles.forEach(file => {
            this.files.set(file.name, file);
        });

        this.updateFileInfo(validFiles);
        this.resetProgress();
        document.getElementById('processBtn').disabled = false;
    }

    previewFile(file) {
        if (file.type.startsWith('image/')) {
            this.imagePreview.show(file);
        } else {
            // 如果是Markdown文件，可以显示文本预览
            const reader = new FileReader();
            reader.onload = (e) => {
                Swal.fire({
                    title: file.name,
                    html: `<pre class="text-left"><code>${e.target.result}</code></pre>`,
                    width: '80%',
                    customClass: {
                        container: document.body.classList.contains('dark') ? 'dark-mode' : ''
                    }
                });
            };
            reader.readAsText(file);
        }
    }

    updateFileInfo(files) {
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';

        files.forEach(file => {
            const template = document.getElementById('fileItemTemplate');
            const fileItem = document.importNode(template.content, true);

            fileItem.querySelector('.file-info-name').textContent = file.name;
            fileItem.querySelector('.file-info-size').textContent = this.formatFileSize(file.size);

            // 根据文件类型设置不同的图标
            const iconSvg = fileItem.querySelector('.file-icon');
            if (file.type.startsWith('image/')) {
                iconSvg.innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                `;
            }

            fileList.appendChild(fileItem);
        });

        document.getElementById('fileInfo').classList.remove('hidden');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showError(message) {
        Swal.fire({
            icon: 'error',
            title: '错误',
            text: message,
            customClass: {
                container: document.body.classList.contains('dark') ? 'dark-mode' : ''
            }
        });
    }

    async processFiles() {
        const fileInput = document.getElementById('fileInput');
        const files = fileInput.files;
        
        if (files.length === 0) {
            this.showError('请先选择文件');
            return;
        }

        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });

        try {
            document.getElementById('processBtn').disabled = true;
            document.getElementById('statusIndicator').className = 'status-indicator processing';
            document.getElementById('statusText').textContent = '处理中...';

            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('处理请求失败');
            }

            const result = await response.json();
            this.wsManager.sendMessage({ task_id: result.task_id });

        } catch (error) {
            this.showError(error.message);
            document.getElementById('processBtn').disabled = false;
        }
    }

    resetProgress() {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        progressBar.style.width = '0%';
        progressText.textContent = '准备处理...';
        statusIndicator.className = 'status-indicator';
        statusText.textContent = '等待处理';
        
        document.getElementById('results').innerHTML = '';
    }
}

// 全局变量
let currentFile = null;
let isProcessing = false;

// 进度条和加载状态管理
function updateProgress(percent, status) {
    const progressBar = document.getElementById('progressBar');
    const progressPercentage = document.getElementById('progressPercentage');
    const progressStatus = document.getElementById('progressStatus');
    const progressArea = document.getElementById('progressArea');

    if (percent === 0) {
        progressArea.classList.remove('hidden');
    }

    progressBar.style.width = `${percent}%`;
    progressPercentage.textContent = `${percent}%`;
    if (status) {
        progressStatus.textContent = status;
    }

    if (percent === 100) {
        setTimeout(() => {
            progressArea.classList.add('hidden');
        }, 1000);
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    const wsManager = new WebSocketManager();
    wsManager.connect();
    
    const fileProcessor = new FileProcessor(wsManager);
    
    // 深色模式切换
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });

    // 恢复深色模式设置
    if (localStorage.getItem('darkMode') === 'true') {
        document.documentElement.classList.add('dark');
    }
});
