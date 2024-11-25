window.app = {
    setupThemeToggle() {
        const darkModeToggle = document.getElementById('dark-mode-toggle');
        const html = document.documentElement;
        
        // 检查本地存储中的主题设置
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            html.classList.add('dark');
        }

        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem('theme')) {
                if (e.matches) {
                    html.classList.add('dark');
                } else {
                    html.classList.remove('dark');
                }
            }
        });

        // 切换按钮点击事件
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', () => {
                if (html.classList.contains('dark')) {
                    html.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                } else {
                    html.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                }
            });
        }
    },

    async downloadFile(downloadUrl) {
        try {
            const response = await fetch(downloadUrl);
            const blob = await response.blob();
            const filename = response.headers.get('Content-Disposition')?.split('filename=')[1]?.replace(/"/g, '') || 'processed_markdown.md';
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Download error:', error);
            this.showError('下载文件失败');
        }
    },

    showError(message) {
        Swal.fire({
            title: '错误',
            text: message,
            icon: 'error',
            confirmButtonText: '确定'
        });
    },

    showSuccess(message) {
        Swal.fire({
            title: '成功',
            text: message,
            icon: 'success',
            confirmButtonText: '确定'
        });
    },

    setupDropZone() {
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');

        if (!dropZone || !fileInput) return;

        // 处理拖放事件
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        // 拖放视觉反馈
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900/20');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900/20');
            });
        });

        // 处理文件拖放
        dropZone.addEventListener('drop', (e) => {
            const file = e.dataTransfer.files[0];
            if (file) {
                this.handleFile(file);
            }
        });

        // 处理文件选择
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleFile(file);
            }
        });

        // 点击区域触发文件选择
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
    },

    setupUrlSection() {
        const urlInput = document.getElementById('url-input');
        const urlSubmitBtn = document.getElementById('url-submit');
        
        if (urlSubmitBtn) {
            urlSubmitBtn.addEventListener('click', () => {
                const url = urlInput.value.trim();
                if (url) {
                    this.handleUrl(url);
                } else {
                    this.showError('请输入有效的URL');
                }
            });
        }
    },

    setupSwitchButtons() {
        const mdFileBtn = document.getElementById('md-file-btn');
        const urlBtn = document.getElementById('url-btn');
        const mdFileSection = document.getElementById('md-file-section');
        const urlSection = document.getElementById('url-section');

        if (!mdFileBtn || !urlBtn || !mdFileSection || !urlSection) return;

        mdFileBtn.addEventListener('click', () => {
            mdFileSection.classList.remove('hidden');
            urlSection.classList.add('hidden');
            mdFileBtn.classList.add('bg-blue-600', 'text-white');
            mdFileBtn.classList.remove('bg-gray-100', 'text-gray-700');
            urlBtn.classList.remove('bg-blue-600', 'text-white');
            urlBtn.classList.add('bg-gray-100', 'text-gray-700');
        });

        urlBtn.addEventListener('click', () => {
            mdFileSection.classList.add('hidden');
            urlSection.classList.remove('hidden');
            urlBtn.classList.add('bg-blue-600', 'text-white');
            urlBtn.classList.remove('bg-gray-100', 'text-gray-700');
            mdFileBtn.classList.remove('bg-blue-600', 'text-white');
            mdFileBtn.classList.add('bg-gray-100', 'text-gray-700');
        });
    },

    async handleFile(file) {
        if (!file.name.toLowerCase().endsWith('.md')) {
            this.showError('请选择Markdown文件（.md）');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                if (result.download_url) {
                    await this.downloadFile(result.download_url);
                    this.showSuccess('文件处理成功！');
                } else {
                    this.showError('处理成功但未返回下载链接');
                }
            } else {
                const error = await response.text();
                this.showError(`上传失败: ${error}`);
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showError('文件上传失败');
        }
    },

    async handleUrl(url) {
        try {
            const response = await fetch('/process_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            if (response.ok) {
                const result = await response.json();
                if (result.download_url) {
                    await this.downloadFile(result.download_url);
                    this.showSuccess('URL处理成功！');
                } else {
                    this.showError('处理成功但未返回下载链接');
                }
            } else {
                const error = await response.text();
                this.showError(`处理失败: ${error}`);
            }
        } catch (error) {
            console.error('URL processing error:', error);
            this.showError('URL处理失败');
        }
    },

    init() {
        console.log('App initialized');
        this.setupThemeToggle();
        this.setupDropZone();
        this.setupUrlSection();
        this.setupSwitchButtons();
    }
};
