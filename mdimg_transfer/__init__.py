"""
应用初始化模块。
"""

import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def setup_logging(level=None):
    """设置日志配置"""
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 添加文件处理器
    log_file = os.path.join(log_dir, 'mdimg_transfer.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(numeric_level)
    root_logger.addHandler(file_handler)
    
    # 设置一些第三方库的日志级别
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    
    # 输出初始日志消息
    root_logger.info(f"日志系统初始化完成，级别: {level}")
    root_logger.info(f"日志文件路径: {log_file}")

# 在模块导入时设置日志
setup_logging()

# 创建logger
logger = logging.getLogger('mdimg_transfer')
