import asyncio
import os
from dotenv import load_dotenv
from mdimg_transfer.core import ImageProcessor, ImageConfig

# 加载环境变量
load_dotenv()

async def test_image_processing():
    # 创建临时目录
    temp_dir = "temp"
    cache_dir = os.path.join(temp_dir, "cache")
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    
    # 创建图片处理配置
    config = ImageConfig(
        max_width=1920,
        max_height=1080,
        quality=85,
        format='auto',
        optimize=True,
        strip_metadata=True
    )
    
    # 初始化图片处理器
    processor = ImageProcessor(
        temp_dir=temp_dir,
        cache_dir=cache_dir,
        config=config
    )
    
    # 测试图片URL
    test_urls = [
        "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png",  # Python logo
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Markdown-mark.svg/1200px-Markdown-mark.svg.png",  # Markdown logo
    ]
    
    async with processor:
        for url in test_urls:
            print(f"\n处理图片: {url}")
            try:
                # 下载图片
                temp_path, content_type = await processor.download_image(url)
                print(f"下载完成: {temp_path}")
                print(f"内容类型: {content_type}")
                
                # 处理图片
                result = await processor.process_image(temp_path)
                if result.success:
                    print(f"处理完成: {result.output_path}")
                    print(f"处理统计: {result.stats}")
                else:
                    print(f"处理失败: {result.error}")
                    
            except Exception as e:
                print(f"错误: {e}")
        
        # 清理临时文件
        await processor.cleanup_temp_files()

if __name__ == "__main__":
    asyncio.run(test_image_processing())
