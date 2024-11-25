"""
Cloudflare R2 客户端
提供与Cloudflare R2存储交互的功能
"""

import os
import logging
import boto3
from botocore.config import Config
from ..config import Config as AppConfig

logger = logging.getLogger(__name__)

class R2Client:
    """R2客户端类"""
    
    def __init__(self):
        """初始化R2客户端"""
        self.config = AppConfig()
        
        # 配置S3客户端
        self.s3_client = boto3.client(
            service_name='s3',
            endpoint_url=self.config.R2_ENDPOINT,
            aws_access_key_id=self.config.R2_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.R2_SECRET_ACCESS_KEY,
            config=Config(
                retries={'max_attempts': 3},
                connect_timeout=5,
                read_timeout=10
            )
        )
        
    async def upload_file(self, file_path: str, key: str) -> str:
        """
        上传文件到R2
        
        Args:
            file_path: 本地文件路径
            key: R2对象键名
            
        Returns:
            str: 文件的公共访问URL
        """
        try:
            # 获取文件的Content-Type
            content_type = self._get_content_type(file_path)
            
            # 上传文件
            with open(file_path, 'rb') as f:
                self.s3_client.upload_fileobj(
                    f,
                    self.config.R2_BUCKET_NAME,
                    key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'public-read'
                    }
                )
                
            # 返回公共访问URL
            return f"{self.config.R2_PUBLIC_URL}/{key}"
            
        except Exception as e:
            logger.error(f"Error uploading file to R2: {e}")
            raise
            
    def _get_content_type(self, file_path: str) -> str:
        """获取文件的Content-Type"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.md': 'text/markdown',
            '.txt': 'text/plain'
        }
        return content_types.get(ext, 'application/octet-stream')
