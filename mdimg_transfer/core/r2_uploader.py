"""
Cloudflare R2 上传模块
"""
import os
import logging
import boto3
from botocore.config import Config
from ..config import config

logger = logging.getLogger(__name__)

class R2Uploader:
    def __init__(self):
        """初始化 R2 客户端"""
        if not config.R2_ENDPOINT_URL:
            raise ValueError("R2_ENDPOINT_URL is not configured")
            
        self.s3_client = boto3.client(
            's3',
            endpoint_url=config.R2_ENDPOINT_URL,
            aws_access_key_id=config.R2_ACCESS_KEY_ID,
            aws_secret_access_key=config.R2_SECRET_ACCESS_KEY,
            config=Config(
                retries={'max_attempts': 3}
            )
        )
        self.bucket_name = config.R2_BUCKET_NAME
        
    async def upload_image(self, file_path: str, object_name: str) -> str:
        """
        上传图片到 R2
        
        Args:
            file_path: 本地文件路径
            object_name: R2中的对象名称
            
        Returns:
            str: R2 公共访问URL
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            # 获取文件的MIME类型
            content_type = self._get_content_type(file_path)
            
            # 上传文件
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs={'ContentType': content_type}
            )
            
            # 构建公共访问URL
            public_url = f"{config.R2_PUBLIC_URL}/{object_name}"
            logger.info(f"Successfully uploaded image to R2: {public_url}")
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to upload image to R2: {str(e)}", exc_info=True)
            raise
            
    def _get_content_type(self, file_path: str) -> str:
        """获取文件的MIME类型"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
        }
        return content_types.get(ext, 'application/octet-stream')
