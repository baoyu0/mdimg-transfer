"""
配置管理模块。
处理应用配置和存储凭证。
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ImageConfig:
    """图片处理配置"""
    max_width: int = 1920
    max_height: int = 1080
    quality: int = 85
    format: str = 'auto'  # auto, jpeg, png, webp
    optimize: bool = True
    strip_metadata: bool = True
    max_file_size: int = 50 * 1024 * 1024  # 50MB

class Config:
    """配置管理器"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config: Dict[str, Any] = {}
        self.storage_config: Dict[str, Dict[str, Any]] = {}
        
        # 加载环境变量
        load_dotenv()
        
        # 设置默认配置
        self.config.update({
            'temp_dir': 'temp',
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'allowed_extensions': ['.md', '.markdown'],
            'image_processing': ImageConfig().__dict__
        })
    
    def load_storage_config(self, config_file: Optional[str] = None) -> None:
        """
        加载存储配置。
        
        Args:
            config_file: 配置文件路径，如果为 None 则使用默认路径
        """
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'storage.json')
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.storage_config = json.load(f)
                logger.info(f"Loaded storage config from {config_file}")
            else:
                logger.warning(f"Storage config file not found: {config_file}")
                
        except Exception as e:
            logger.error(f"Error loading storage config: {e}")
            raise
    
    def get_storage_credentials(self, provider: str) -> Dict[str, Any]:
        """
        获取存储提供者的凭证。
        优先使用环境变量，然后使用配置文件。
        
        Args:
            provider: 存储提供者名称
            
        Returns:
            Dict[str, Any]: 凭证信息
        """
        credentials = {}
        
        # 从环境变量获取凭证
        env_prefix = f"{provider.upper()}_"
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                credentials[key[len(env_prefix):].lower()] = value
        
        # 如果环境变量中没有凭证，使用配置文件
        if not credentials and provider in self.storage_config:
            credentials = self.storage_config[provider].get('credentials', {})
        
        return credentials
    
    def get_storage_config(self, provider: str) -> Dict[str, Any]:
        """
        获取存储提供者的配置。
        
        Args:
            provider: 存储提供者名称
            
        Returns:
            Dict[str, Any]: 配置信息
        """
        return self.storage_config.get(provider, {}).get('config', {})
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值。
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置值。
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
        
    def save(self) -> None:
        """保存配置到文件"""
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        # 保存主配置
        config_file = os.path.join(config_dir, 'config.json')
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # 保存存储配置
        storage_file = os.path.join(config_dir, 'storage.json')
        with open(storage_file, 'w') as f:
            json.dump(self.storage_config, f, indent=2)
