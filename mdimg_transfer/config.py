import os
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path

@dataclass
class Config:
    # 数据库配置
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///mdimg.db')
    
    # Cloudflare R2配置
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    BUCKET_NAME: str = os.getenv('BUCKET_NAME', '')
    PUBLIC_URL: str = os.getenv('PUBLIC_URL', '')
    R2_ENDPOINT_URL: str = os.getenv('R2_ENDPOINT_URL', '')
    R2_ENDPOINT: str = R2_ENDPOINT_URL  # 添加别名
    R2_ACCESS_KEY_ID: str = os.getenv('R2_ACCESS_KEY_ID', '')
    R2_SECRET_ACCESS_KEY: str = os.getenv('R2_SECRET_ACCESS_KEY', '')
    R2_BUCKET_NAME: str = os.getenv('R2_BUCKET_NAME', '')
    R2_PUBLIC_URL: str = os.getenv('R2_PUBLIC_URL', '')  # R2 bucket 的公共访问URL
    
    # 文件路径配置
    BASE_DIR: str = str(Path(__file__).parent.parent)
    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, os.getenv('UPLOAD_FOLDER', 'uploads'))
    PROCESSED_FOLDER: str = os.path.join(BASE_DIR, os.getenv('PROCESSED_FOLDER', 'processed'))
    IMAGE_FOLDER: str = os.path.join(BASE_DIR, os.getenv('IMAGE_FOLDER', 'images'))
    TEMP_DIR: str = os.path.join(BASE_DIR, os.getenv('TEMP_DIR', 'temp'))  # 添加临时目录配置
    temp_dir: str = TEMP_DIR  # 添加小写别名
    
    # 应用配置
    MAX_FILE_SIZE: int = int(str(os.getenv('MAX_FILE_SIZE', 50 * 1024 * 1024)).strip())  # 默认50MB
    MAX_CONCURRENT_DOWNLOADS: int = int(str(os.getenv('MAX_CONCURRENT_DOWNLOADS', 5)).strip())
    DOWNLOAD_TIMEOUT: int = int(str(os.getenv('DOWNLOAD_TIMEOUT', 30)).strip())
    MAX_RETRIES: int = int(str(os.getenv('MAX_RETRIES', 3)).strip())
    
    # 图片处理配置
    MAX_IMAGE_WIDTH: int = int(os.getenv('MAX_IMAGE_WIDTH', 1920))
    MAX_IMAGE_HEIGHT: int = int(os.getenv('MAX_IMAGE_HEIGHT', 1080))
    IMAGE_QUALITY: int = int(os.getenv('IMAGE_QUALITY', 85))
    ALLOWED_MIME_TYPES: List[str] = field(default_factory=lambda: [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/bmp',
        'image/tiff'
    ])
    
    # 监控配置
    METRICS_PORT: int = int(os.getenv('METRICS_PORT', 9090))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR: str = os.path.join(BASE_DIR, 'logs')
    LOG_FILE: str = os.path.join(LOG_DIR, os.getenv('LOG_FILE', 'app.log'))
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    @classmethod
    def validate(cls) -> list[str]:
        """验证配置，返回错误信息列表"""
        errors = []
        
        # 验证必需的配置项
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required")
            
        # 验证数值范围
        if not (0 < cls.MAX_FILE_SIZE <= 100 * 1024 * 1024):
            errors.append("MAX_FILE_SIZE must be between 0 and 100MB")
            
        if not (1 <= cls.MAX_CONCURRENT_DOWNLOADS <= 10):
            errors.append("MAX_CONCURRENT_DOWNLOADS must be between 1 and 10")
            
        if not (5 <= cls.DOWNLOAD_TIMEOUT <= 60):
            errors.append("DOWNLOAD_TIMEOUT must be between 5 and 60 seconds")
            
        if not (1 <= cls.MAX_RETRIES <= 5):
            errors.append("MAX_RETRIES must be between 1 and 5")
            
        if not (0 < cls.IMAGE_QUALITY <= 100):
            errors.append("IMAGE_QUALITY must be between 1 and 100")
            
        return errors

config = Config()
