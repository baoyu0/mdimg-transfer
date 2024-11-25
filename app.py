"""
应用程序配置和创建。
"""
import logging
import os
from pathlib import Path
from quart import Quart, render_template, send_from_directory
from mdimg_transfer.config import config
from mdimg_transfer.routes.api import api
from mdimg_transfer.core.markdown_processor import MarkdownProcessor
from mdimg_transfer.core.image_downloader import ImageDownloader
from mdimg_transfer.core.r2_uploader import R2Uploader
from mdimg_transfer.core.html_converter import HTMLConverter

def setup_logging():
    """配置日志系统"""
    log_dir = Path(config.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成，级别: %s", logging.getLevelName(logging.DEBUG))
    logger.info("日志文件路径: %s", config.LOG_FILE)
    return logger

def create_app():
    """创建并配置应用实例"""
    app = Quart(__name__, 
                static_folder='static',
                static_url_path='')
    
    # 配置日志
    logger = setup_logging()
    logger.info("正在创建应用实例...")
    
    # 确保必要的目录存在
    for folder in [config.UPLOAD_FOLDER, config.PROCESSED_FOLDER, 
                  config.IMAGE_FOLDER, config.TEMP_DIR]:
        Path(folder).mkdir(exist_ok=True)
        logger.debug("已创建目录: %s", folder)
    
    logger.debug("正在创建依赖组件...")
    
    # 创建依赖组件
    image_downloader = ImageDownloader()
    r2_uploader = R2Uploader()
    html_converter = HTMLConverter()
    
    logger.debug("正在创建 MarkdownProcessor 实例...")
    markdown_processor = MarkdownProcessor(image_downloader, r2_uploader)
    
    logger.debug("正在注册蓝图...")
    # 注册蓝图
    app.register_blueprint(api.create_blueprint(markdown_processor, html_converter), url_prefix='/api')
    
    @app.route('/')
    async def index():
        """主页"""
        return await render_template('index.html')
    
    @app.route('/download/<path:filename>')
    async def download_file(filename):
        return await send_from_directory('processed', filename)
    
    logger.info("应用实例创建完成")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
