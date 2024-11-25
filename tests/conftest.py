import pytest
import os
import tempfile
import shutil

@pytest.fixture(scope="session")
def test_dir():
    """创建测试目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """设置测试环境变量"""
    monkeypatch.setenv('DATABASE_URL', 'sqlite+aiosqlite:///test.db')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test_key')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test_secret')
    monkeypatch.setenv('BUCKET_NAME', 'test-bucket')
    monkeypatch.setenv('PUBLIC_URL', 'https://test.example.com')
    monkeypatch.setenv('MAX_FILE_SIZE', '52428800')  # 50MB
    monkeypatch.setenv('MAX_CONCURRENT_DOWNLOADS', '5')
    monkeypatch.setenv('DOWNLOAD_TIMEOUT', '30')
    monkeypatch.setenv('MAX_RETRIES', '3')
    monkeypatch.setenv('MAX_IMAGE_WIDTH', '1920')
    monkeypatch.setenv('MAX_IMAGE_HEIGHT', '1080')
    monkeypatch.setenv('IMAGE_QUALITY', '85')
    monkeypatch.setenv('METRICS_PORT', '9090')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')
    monkeypatch.setenv('LOG_FILE', 'test.log')
