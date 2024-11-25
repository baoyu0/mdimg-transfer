"""
应用程序配置和创建。
"""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from quart import Quart, send_from_directory, render_template
from .config import config
from .routes.api import bp as api
from .core.markdown_processor import MarkdownProcessor
from .core.image_downloader import ImageDownloader
from .core.r2_uploader import R2Uploader
from .core.html_converter import HTMLConverter

def setup_logging():
    """配置日志系统"""
    # 确保日志目录存在
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # 创建日志格式
    formatter = logging.Formatter(config.LOG_FORMAT)
    
    # 获取日志级别
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # 添加文件处理器
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root_logger.addHandler(file_handler)
    
    # 创建应用日志记录器
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成，级别: %s", logging.getLevelName(log_level))
    logger.info("日志文件路径: %s", config.LOG_FILE)
    
    return logger

def create_app():
    """创建并配置应用实例"""
    # 设置日志
    logger = setup_logging()
    logger.info("正在创建应用实例...")
    
    # 创建应用实例
    app = Quart("mdimg_transfer", static_folder="../static", template_folder="../templates")
    
    # 确保必要的目录存在
    for folder in [config.UPLOAD_FOLDER, config.PROCESSED_FOLDER, 
                  config.IMAGE_FOLDER, config.TEMP_DIR]:
        Path(folder).mkdir(exist_ok=True)
        logger.debug("已创建目录: %s", folder)
    
    # 创建依赖组件
    logger.debug("正在创建依赖组件...")
    downloader = ImageDownloader()
    r2_uploader = R2Uploader()
    html_converter = HTMLConverter()
    
    # 创建 MarkdownProcessor 实例
    logger.debug("正在创建 MarkdownProcessor 实例...")
    processor = MarkdownProcessor(downloader=downloader, r2_uploader=r2_uploader)
    app.processor = processor
    app.html_converter = html_converter
    
    # 注册蓝图
    logger.debug("正在注册蓝图...")
    app.register_blueprint(api)
    
    @app.route('/')
    async def index():
        """主页"""
        return await render_template('index.html')
        
    @app.route('/static/<path:filename>')
    async def static_files(filename):
        """静态文件"""
        return await send_from_directory('../static', filename)

    @app.route('/css/<path:filename>')
    async def css_files(filename):
        """CSS文件"""
        return await send_from_directory('../static/css', filename)
    
    logger.info("应用实例创建完成")
    return app

# 创建应用实例
app = create_app()
