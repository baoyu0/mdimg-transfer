"""
存储管理模块。
提供云存储服务的统一接口。
"""

import os
import shutil
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple
import boto3
from botocore.exceptions import ClientError
from pathlib import Path

logger = logging.getLogger(__name__)

class StorageProvider(ABC):
    """存储提供者基类"""
    
    @abstractmethod
    async def upload_file(self, file_path: str, destination_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        上传文件到存储服务。
        
        Args:
            file_path: 本地文件路径
            destination_path: 目标路径
            
        Returns:
            Tuple[Optional[str], Optional[str]]:
            (文件URL, 错误信息)
        """
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> Optional[str]:
        """
        从存储服务删除文件。
        
        Args:
            file_path: 文件路径
            
        Returns:
            Optional[str]: 错误信息
        """
        pass

class LocalStorageProvider(StorageProvider):
    """本地文件系统存储提供者"""
    
    def __init__(self, base_dir: str = "storage", base_url: str = "/storage"):
        """
        初始化本地存储提供者。
        
        Args:
            base_dir: 基础存储目录
            base_url: 基础URL路径
        """
        self.base_dir = Path(base_dir)
        self.base_url = base_url
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    async def upload_file(self, file_path: str, destination_path: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            # 确保目标目录存在
            dest_path = self.base_dir / destination_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            shutil.copy2(file_path, dest_path)
            
            # 生成URL
            url = f"{self.base_url}/{destination_path}"
            return url, None
            
        except Exception as e:
            error_message = f"Error copying file: {str(e)}"
            logger.error(error_message)
            return None, error_message
    
    async def delete_file(self, file_path: str) -> Optional[str]:
        try:
            full_path = self.base_dir / file_path
            if full_path.exists():
                full_path.unlink()
            return None
            
        except Exception as e:
            error_message = f"Error deleting file: {str(e)}"
            logger.error(error_message)
            return error_message

class S3StorageProvider(StorageProvider):
    """AWS S3 存储提供者"""
    
    def __init__(self, bucket_name: str, **kwargs):
        """
        初始化 S3 存储提供者。
        
        Args:
            bucket_name: S3 存储桶名称
            **kwargs: 其他 S3 客户端配置参数
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', **kwargs)
        
    async def upload_file(self, file_path: str, destination_path: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            # 上传文件到 S3
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                destination_path
            )
            
            # 生成文件 URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{destination_path}"
            return url, None
            
        except ClientError as e:
            error_message = f"Error uploading to S3: {str(e)}"
            logger.error(error_message)
            return None, error_message
        
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(error_message)
            return None, error_message
    
    async def delete_file(self, file_path: str) -> Optional[str]:
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return None
            
        except ClientError as e:
            error_message = f"Error deleting from S3: {str(e)}"
            logger.error(error_message)
            return error_message
        
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(error_message)
            return error_message

class StorageManager:
    """存储管理器"""
    
    def __init__(self):
        self.providers: Dict[str, StorageProvider] = {}
        # 注册默认的本地存储提供者
        self.register_provider("local", LocalStorageProvider())
    
    def register_provider(self, name: str, provider: StorageProvider):
        """
        注册存储提供者。
        
        Args:
            name: 提供者名称
            provider: 存储提供者实例
        """
        self.providers[name] = provider
    
    def get_provider(self, name: str) -> Optional[StorageProvider]:
        """
        获取存储提供者。
        
        Args:
            name: 提供者名称
            
        Returns:
            Optional[StorageProvider]: 存储提供者实例
        """
        return self.providers.get(name)
    
    async def transfer_file(self,
                          file_path: str,
                          source_provider: str,
                          destination_provider: str,
                          destination_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        在不同存储提供者之间传输文件。
        如果源提供者是 "source"，则直接从本地文件上传。
        
        Args:
            file_path: 文件路径
            source_provider: 源存储提供者名称
            destination_provider: 目标存储提供者名称
            destination_path: 目标路径
            
        Returns:
            Tuple[Optional[str], Optional[str]]:
            (目标文件URL, 错误信息)
        """
        # 如果源是 "source"，表示直接从本地文件上传
        if source_provider == "source":
            dst_provider = self.get_provider(destination_provider or "local")
            if not dst_provider:
                return None, f"Destination provider '{destination_provider}' not found"
            
            return await dst_provider.upload_file(file_path, destination_path)
        
        # 正常的提供者之间传输
        src_provider = self.get_provider(source_provider)
        dst_provider = self.get_provider(destination_provider)
        
        if not src_provider:
            return None, f"Source provider '{source_provider}' not found"
        
        if not dst_provider:
            return None, f"Destination provider '{destination_provider}' not found"
        
        try:
            # 上传到目标存储
            url, error = await dst_provider.upload_file(file_path, destination_path)
            if error:
                return None, error
            
            return url, None
            
        except Exception as e:
            error_message = f"Error transferring file: {str(e)}"
            logger.error(error_message)
            return None, error_message
