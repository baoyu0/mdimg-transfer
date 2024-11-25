import pytest
import os
import asyncio
import aiohttp
from unittest.mock import Mock, patch
from mdimg_transfer.core.image_processing import ImageDownloader
from mdimg_transfer.core.models import ProcessingHistory

@pytest.fixture
def temp_dir(tmp_path):
    return str(tmp_path)

@pytest.fixture
async def mock_session():
    """模拟aiohttp会话"""
    class MockResponse:
        def __init__(self, status, content):
            self.status = status
            self.content = content
            
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
        async def read(self):
            return self.content.chunks[0]
    
    class MockContent:
        def __init__(self, chunks):
            self.chunks = chunks
            self.current = 0
            
        async def iter_chunked(self, size):
            for chunk in self.chunks:
                yield chunk
    
    class MockClientSession:
        def __init__(self):
            self.get_responses = {}
            
        def set_response(self, url, status, chunks):
            content = MockContent(chunks)
            self.get_responses[url] = MockResponse(status, content)
            
        async def get(self, url, **kwargs):
            return self.get_responses.get(url, MockResponse(404, None))
            
        async def close(self):
            pass
            
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
    
    return MockClientSession()

@pytest.fixture
async def mock_db_session():
    """模拟数据库会话"""
    class MockDBSession:
        def __init__(self):
            self.records = []
            
        async def add(self, record):
            self.records.append(record)
            
        async def commit(self):
            pass
            
        async def rollback(self):
            pass
            
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
    
    session = MockDBSession()
    return session

@pytest.mark.asyncio
async def test_download_single_image(temp_dir, mock_session, mock_db_session):
    """测试单个图片下载"""
    # 设置模拟响应
    test_url = "http://example.com/test.jpg"
    test_content = b"fake image content"
    mock_session.set_response(test_url, 200, [test_content])
    
    # 创建下载器实例
    downloader = ImageDownloader(temp_dir)
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        result = await downloader._download_single_image(test_url)
    
    assert result is not None
    assert len(mock_db_session.records) == 1
    assert mock_db_session.records[0].status == 'success'

@pytest.mark.asyncio
async def test_download_invalid_image(temp_dir, mock_session, mock_db_session):
    """测试下载无效图片"""
    # 设置模拟响应
    test_url = "http://example.com/invalid.jpg"
    mock_session.set_response(test_url, 404, [])
    
    # 创建下载器实例
    downloader = ImageDownloader(temp_dir)
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        result = await downloader._download_single_image(test_url)
    
    assert result is None
    assert len(mock_db_session.records) == 1
    assert mock_db_session.records[0].status == 'failed'

@pytest.mark.asyncio
async def test_download_multiple_images(temp_dir, mock_session, mock_db_session):
    """测试多个图片并发下载"""
    # 设置模拟响应
    urls = [
        "http://example.com/1.jpg",
        "http://example.com/2.jpg",
        "http://example.com/3.jpg"
    ]
    test_content = b"fake image content"
    for url in urls:
        mock_session.set_response(url, 200, [test_content])
    
    # 创建下载器实例
    downloader = ImageDownloader(temp_dir)
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        results = await downloader.download_images(urls)
    
    assert all(results.values())
    assert len(mock_db_session.records) == len(urls)
    assert all(record.status == 'success' for record in mock_db_session.records)

@pytest.mark.asyncio
async def test_file_size_limit(temp_dir, mock_session, mock_db_session):
    """测试文件大小限制"""
    # 设置模拟响应
    test_url = "http://example.com/large.jpg"
    large_content = b"x" * (50 * 1024 * 1024 + 1)  # 超过50MB
    mock_session.set_response(test_url, 200, [large_content])
    
    # 创建下载器实例
    downloader = ImageDownloader(temp_dir)
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        result = await downloader._download_single_image(test_url)
    
    assert result is None
    assert len(mock_db_session.records) == 1
    assert mock_db_session.records[0].status == 'failed'
    assert 'file too large' in mock_db_session.records[0].error_message.lower()

@pytest.mark.asyncio
async def test_image_processing_config():
    """测试图片处理配置"""
    from mdimg_transfer.core.image_processing import ImageConfig
    
    config = ImageConfig(
        max_width=800,
        max_height=600,
        quality=85,
        format='JPEG',
        strip_metadata=True
    )
    
    assert config.max_width == 800
    assert config.max_height == 600
    assert config.quality == 85
    assert config.format == 'JPEG'
    assert config.strip_metadata is True

@pytest.mark.asyncio
async def test_image_processing(temp_dir):
    """测试图片处理功能"""
    from mdimg_transfer.core.image_processing import ImageProcessor
    from PIL import Image
    import io
    
    # 创建测试图片
    test_image = Image.new('RGB', (1200, 900), color='red')
    image_bytes = io.BytesIO()
    test_image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    
    # 创建处理器实例
    processor = ImageProcessor()
    config = ImageConfig(max_width=800, max_height=600)
    
    # 处理图片
    result = await processor.process_image(image_bytes.getvalue(), config)
    
    # 验证结果
    processed_image = Image.open(io.BytesIO(result.image_data))
    assert processed_image.size[0] <= 800
    assert processed_image.size[1] <= 600
    assert result.format == 'JPEG'
    assert result.size < len(image_bytes.getvalue())

@pytest.mark.asyncio
async def test_cache_functionality(temp_dir):
    """测试缓存功能"""
    from mdimg_transfer.core.cache import AsyncLRUCache, cached
    
    cache = AsyncLRUCache(max_size=100)
    
    @cached(cache)
    async def process_with_cache(url: str) -> str:
        return f"processed_{url}"
    
    # 首次调用
    result1 = await process_with_cache("test.jpg")
    assert result1 == "processed_test.jpg"
    
    # 从缓存获取
    result2 = await process_with_cache("test.jpg")
    assert result2 == "processed_test.jpg"
    assert cache.hits == 1
    assert cache.misses == 1

@pytest.mark.asyncio
async def test_retry_mechanism(temp_dir, mock_session, mock_db_session):
    """测试重试机制"""
    from mdimg_transfer.errors.retry import RetryConfig, with_retry
    
    retry_count = 0
    
    @with_retry(RetryConfig(max_retries=3, delay=0.1))
    async def failing_download():
        nonlocal retry_count
        retry_count += 1
        raise ConnectionError("Network error")
    
    with pytest.raises(ConnectionError):
        await failing_download()
    
    assert retry_count == 4  # 初始尝试 + 3次重试

@pytest.mark.asyncio
async def test_concurrent_downloads(temp_dir, mock_session, mock_db_session):
    """测试并发下载限制"""
    from mdimg_transfer.core.image_processing import ImageDownloader
    import asyncio
    
    # 创建多个URL
    urls = [f"http://example.com/image_{i}.jpg" for i in range(10)]
    test_content = b"fake image content"
    for url in urls:
        mock_session.set_response(url, 200, [test_content])
    
    # 设置并发限制
    downloader = ImageDownloader(temp_dir, concurrent_limit=3)
    
    start_time = asyncio.get_event_loop().time()
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        results = await downloader.download_images(urls)
    end_time = asyncio.get_event_loop().time()
    
    # 验证所有下载都成功
    assert all(results.values())
    # 验证并发限制生效（至少需要4轮下载）
    assert end_time - start_time >= 0.3  # 假设每次下载至少需要0.1秒

@pytest.mark.asyncio
async def test_progress_tracking(temp_dir, mock_session, mock_db_session):
    """测试进度跟踪"""
    from mdimg_transfer.core.image_processing import ImageDownloader
    
    progress_updates = []
    
    def progress_callback(current, total):
        progress_updates.append((current, total))
    
    # 设置测试URL和内容
    urls = [f"http://example.com/progress_{i}.jpg" for i in range(5)]
    test_content = b"fake image content"
    for url in urls:
        mock_session.set_response(url, 200, [test_content])
    
    # 创建下载器实例
    downloader = ImageDownloader(temp_dir, progress_callback=progress_callback)
    async with mock_session as session, mock_db_session as db_session:
        downloader.session = session
        downloader.db_session = db_session
        results = await downloader.download_images(urls)
    
    # 验证进度更新
    assert len(progress_updates) == len(urls)
    assert progress_updates[-1] == (5, 5)  # 最后一次更新应该是完成状态
