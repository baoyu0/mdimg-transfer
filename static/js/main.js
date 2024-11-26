// 应用主程序对象
const app = {
    init() {
        console.log('Initializing app...');
        this.setupThemeToggle();
        this.setupTabs();
        this.setupFileUpload();
        this.setupUrlSection();
        this.setupWebSocket();
    },

    setupThemeToggle() {
        console.log('Setting up theme toggle...');
        const darkModeToggle = document.getElementById('dark-mode-toggle');
        const html = document.documentElement;

        // 检查系统主题
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            html.classList.add('dark');
        }

        // 检查本地存储的主题设置
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            if (savedTheme === 'dark') {
                html.classList.add('dark');
            } else {
                html.classList.remove('dark');
            }
        }

        darkModeToggle.addEventListener('click', () => {
            html.classList.toggle('dark');
            localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
        });
    },

    setupUrlSection() {
        console.log('Setting up URL section...');
        const urlInput = document.getElementById('urlInput');
        const convertBtn = document.getElementById('convertBtn');
        const convertBtnText = document.getElementById('convertBtnText');
        const convertBtnSpinner = document.getElementById('convertBtnSpinner');

        if (!urlInput || !convertBtn || !convertBtnText || !convertBtnSpinner) {
            console.error('URL section elements not found');
            return;
        }

        convertBtn.addEventListener('click', async () => {
            const url = urlInput.value.trim();
            if (!url) {
                Swal.fire({
                    icon: 'error',
                    title: '错误',
                    text: '请输入要转换的URL'
                });
                return;
            }

            // Show loading state
            convertBtn.disabled = true;
            convertBtnText.classList.add('hidden');
            convertBtnSpinner.classList.remove('hidden');

            try {
                const response = await fetch('/api/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url })
                });

                if (!response.ok) {
                    throw new Error('URL转换失败');
                }

                const result = await response.json();
                
                Swal.fire({
                    icon: 'success',
                    title: '转换成功',
                    text: '文件已成功转换'
                });

                if (result.downloadUrl) {
                    this.createDownloadLink(result.downloadUrl, 'converted.md');
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: '转换失败',
                    text: error.message
                });
            } finally {
                convertBtn.disabled = false;
                convertBtnText.classList.remove('hidden');
                convertBtnSpinner.classList.add('hidden');
            }
        });
    },

    setupWebSocket() {
        console.log('Setting up WebSocket...');
        function generateClientId() {
            return Math.random().toString(36).substring(2, 11);
        }
        const clientId = generateClientId();
        const ws = new WebSocket(`ws://${window.location.host}/ws/${clientId}`);

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('WebSocket message:', data);

            // 更新进度条
            if (data.type === 'progress') {
                this.updateProgress(data.progress);
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };
    },

    updateProgress(progress) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const uploadProgress = document.getElementById('upload-progress');

        if (progress.total > 0) {
            uploadProgress.classList.remove('hidden');
            const percentage = Math.round((progress.current / progress.total) * 100);
            progressBar.style.width = `${percentage}%`;
            progressText.textContent = `${percentage}%`;
        }
    },

    setupFileUpload() {
        console.log('Setting up file upload...');
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-upload');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const uploadProgress = document.getElementById('upload-progress');

        // Check if required elements exist
        if (!dropZone || !fileInput) {
            console.error('File upload elements not found');
            return;
        }

        // Handle file drag and drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-blue-500', 'dark:border-blue-400');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-blue-500', 'dark:border-blue-400');
        });

        dropZone.addEventListener('drop', async (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-blue-500', 'dark:border-blue-400');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                await this.handleFileUpload(files[0]);
            }
        });

        // Handle file selection
        fileInput.addEventListener('change', async () => {
            if (fileInput.files.length > 0) {
                await this.handleFileUpload(fileInput.files[0]);
            }
        });

        // Store progress elements for later use
        this.progressElements = {
            progressBar,
            progressText,
            uploadProgress
        };

        // Handle file upload
        this.handleFileUpload = async (file) => {
            if (!file.name.toLowerCase().endsWith('.md') && !file.name.toLowerCase().endsWith('.markdown')) {
                Swal.fire({
                    icon: 'error',
                    title: '文件类型错误',
                    text: '请选择 .md 或 .markdown 文件'
                });
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            this.progressElements.uploadProgress.classList.remove('hidden');
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }

                // 显示成功消息
                Swal.fire({
                    icon: 'success',
                    title: '上传成功',
                    text: `已成功处理 ${data.successful_downloads} 张图片`,
                    footer: `<a href="${data.download_url}" class="text-blue-500 hover:text-blue-600">点击下载处理后的文件</a>`
                });

            } catch (error) {
                console.error('Error uploading file:', error);
                Swal.fire({
                    icon: 'error',
                    title: '上传失败',
                    text: error.message
                });
            } finally {
                this.progressElements.uploadProgress.classList.add('hidden');
                this.progressElements.progressBar.style.width = '0%';
                this.progressElements.progressText.textContent = '0%';
            }
        }
    },

    setupTabs() {
        console.log('Setting up tabs...');
        const fileTabBtn = document.getElementById('fileTabBtn');
        const urlTabBtn = document.getElementById('urlTabBtn');
        const fileSection = document.getElementById('md-file-section');
        const urlSection = document.getElementById('urlSection');

        // Check if all required elements exist
        if (!fileTabBtn || !urlTabBtn || !fileSection || !urlSection) {
            console.error('Tab elements not found');
            return;
        }

        // Set initial state
        fileTabBtn.classList.add('active');
        urlTabBtn.classList.remove('active');
        fileSection.classList.remove('hidden');
        urlSection.classList.add('hidden');

        // Add click handlers
        fileTabBtn.addEventListener('click', () => {
            fileTabBtn.classList.add('active');
            urlTabBtn.classList.remove('active');
            fileSection.classList.remove('hidden');
            urlSection.classList.add('hidden');
        });

        urlTabBtn.addEventListener('click', () => {
            urlTabBtn.classList.add('active');
            fileTabBtn.classList.remove('active');
            urlSection.classList.remove('hidden');
            fileSection.classList.add('hidden');
        });
    },

    showError(message) {
        Swal.fire({
            icon: 'error',
            title: '错误',
            text: message,
            confirmButtonText: '确定'
        });
    },

    showSuccess(title, message) {
        Swal.fire({
            icon: 'success',
            title: title,
            text: message,
            confirmButtonText: '确定'
        });
    },

    createDownloadLink(downloadUrl, filename) {
        const downloadContainer = document.getElementById('downloadContainer');
        if (downloadContainer) {
            downloadContainer.innerHTML = '';
            
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.className = 'btn btn-success mt-3';
            link.download = filename || 'processed.md';
            link.innerHTML = '<i class="fas fa-download"></i> 下载处理后的文件';
            
            downloadContainer.appendChild(link);
            downloadContainer.style.display = 'block';
        }
    }
};

// 当DOM加载完成时初始化应用
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing app...');
    window.app = app;
    app.init();
});
