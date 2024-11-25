// 应用主程序对象
const app = {
    init() {
        console.log('Initializing app...');
        this.setupThemeToggle();
        this.setupUrlSection();
        this.setupWebSocket();
        
        // 显示URL部分
        const urlSection = document.getElementById('urlSection');
        if (urlSection) {
            urlSection.style.display = 'block';
        }
    },

    setupThemeToggle() {
        console.log('Setting up theme toggle...');
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            // 从localStorage获取主题设置
            const currentTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', currentTheme);
            themeToggle.checked = currentTheme === 'dark';

            // 监听主题切换
            themeToggle.addEventListener('change', () => {
                const newTheme = themeToggle.checked ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                console.log('Theme switched to:', newTheme);
            });
        }
    },

    setupUrlSection() {
        console.log('Setting up URL section...');
        const urlForm = document.getElementById('urlForm');
        const urlInput = document.getElementById('urlInput');
        const convertBtn = document.getElementById('convertUrlBtn');

        if (urlForm && convertBtn) {
            urlForm.onsubmit = (e) => {
                e.preventDefault();
            };

            convertBtn.onclick = async () => {
                const url = urlInput.value.trim();
                if (!url) {
                    this.showError('请输入URL');
                    return;
                }

                try {
                    this.showLoading('正在处理URL...');
                    
                    const response = await fetch('/api/process-url', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ url })
                    });

                    const data = await response.json();
                    console.log('URL processing response:', data);

                    if (!response.ok) {
                        throw new Error(data.error || '处理URL时出错');
                    }

                    if (data.error) {
                        throw new Error(data.error);
                    }

                    if (data.download_url) {
                        this.showSuccess('URL处理成功!', `成功处理 ${data.successful_downloads || 0}/${data.total_images || 0} 张图片`);
                        this.createDownloadLink(data.download_url, data.processed_filename);
                    } else {
                        throw new Error('处理结果中没有下载链接');
                    }

                } catch (error) {
                    console.error('Error processing URL:', error);
                    this.showError(`处理URL失败: ${error.message}`);
                } finally {
                    this.hideLoading();
                }
            };
        }
    },

    setupWebSocket() {
        console.log('Setting up WebSocket...');
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'progress') {
                this.updateProgress(data);
            }
        };
    },

    showLoading(message = '处理中...') {
        const progressContainer = document.getElementById('progressContainer');
        const progressText = document.getElementById('progressText');
        
        if (progressContainer && progressText) {
            progressContainer.style.display = 'block';
            progressText.textContent = message;
            
            // 重置进度条
            const progressBar = document.getElementById('progressBar');
            if (progressBar) {
                progressBar.style.width = '0%';
                progressBar.setAttribute('aria-valuenow', 0);
            }
        }
    },

    hideLoading() {
        const progressContainer = document.getElementById('progressContainer');
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    },

    updateProgress(data) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const progressDetails = document.getElementById('progressDetails');

        if (progressBar && progressText && progressDetails) {
            const percent = Math.round(data.progress * 100);
            progressBar.style.width = `${percent}%`;
            progressBar.setAttribute('aria-valuenow', percent);
            
            progressText.textContent = data.message || '处理中...';
            if (data.details) {
                progressDetails.textContent = data.details;
                progressDetails.style.display = 'block';
            }
        }
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
