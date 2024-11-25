import pytest
from quart import Quart
import io
from mdimg_transfer.app import app as quart_app
from mdimg_transfer.models import ProcessingHistory, init_db, get_session_factory

@pytest.fixture
async def app():
    """创建测试应用实例"""
    app = quart_app
    app.config['TESTING'] = True
    # 初始化测试数据库
    app.db_engine = await init_db('sqlite+aiosqlite:///:memory:')
    app.session_factory = get_session_factory(app.db_engine)
    return app

@pytest.fixture
async def test_client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.mark.asyncio
async def test_process_endpoint_no_file(test_client):
    """测试没有文件的情况"""
    response = await test_client.post('/process')
    assert response.status_code == 400
    data = await response.get_json()
    assert 'error' in data

@pytest.mark.asyncio
async def test_process_endpoint_with_file(test_client):
    """测试上传文件的情况"""
    # 创建测试文件
    data = {
        'file': (io.BytesIO(b'# Test\n![test](http://example.com/test.jpg)'), 'test.md')
    }
    
    response = await test_client.post('/process', files=data)
    assert response.status_code == 200
    data = await response.get_json()
    assert 'message' in data
    assert 'results' in data

@pytest.mark.asyncio
async def test_metrics_endpoint(test_client):
    """测试指标导出端点"""
    # 先添加一些测试数据
    async with test_client.app.session_factory() as session:
        history = ProcessingHistory(
            original_url='http://example.com/test.jpg',
            processed_url='http://cdn.example.com/test.jpg',
            file_size_before=1024,
            file_size_after=512,
            mime_type='image/jpeg',
            status='success',
            processing_time=0.5
        )
        session.add(history)
        await session.commit()
    
    response = await test_client.get('/metrics')
    assert response.status_code == 200
    data = await response.get_json()
    assert 'total_processed' in data
    assert 'success_rate' in data
    assert 'average_processing_time' in data

@pytest.mark.asyncio
async def test_history_endpoint(test_client):
    """测试历史记录端点"""
    # 先添加一些测试数据
    async with test_client.app.session_factory() as session:
        history = ProcessingHistory(
            original_url='http://example.com/test.jpg',
            processed_url='http://cdn.example.com/test.jpg',
            file_size_before=1024,
            file_size_after=512,
            mime_type='image/jpeg',
            status='success',
            processing_time=0.5
        )
        session.add(history)
        await session.commit()
    
    response = await test_client.get('/history')
    assert response.status_code == 200
    data = await response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'original_url' in data[0]
    assert 'status' in data[0]

@pytest.mark.asyncio
async def test_stats_endpoint(test_client):
    """测试统计信息端点"""
    # 先添加一些测试数据
    async with test_client.app.session_factory() as session:
        history = ProcessingHistory(
            original_url='http://example.com/test.jpg',
            processed_url='http://cdn.example.com/test.jpg',
            file_size_before=1024,
            file_size_after=512,
            mime_type='image/jpeg',
            status='success',
            processing_time=0.5
        )
        session.add(history)
        await session.commit()
    
    response = await test_client.get('/stats')
    assert response.status_code == 200
    data = await response.get_json()
    assert 'total_images' in data
    assert 'success_count' in data
    assert 'failure_count' in data
    assert 'total_size' in data
