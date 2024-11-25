import pytest
import os
import asyncio
from PIL import Image
import io
from mdimg_transfer.core.image_processing import ImageProcessor
from concurrent.futures import ThreadPoolExecutor

@pytest.fixture
def image_processor():
    executor = ThreadPoolExecutor(max_workers=2)
    processor = ImageProcessor(executor)
    yield processor
    executor.shutdown()

@pytest.fixture
def sample_image():
    """创建一个示例图片用于测试"""
    img = Image.new('RGB', (2000, 1500), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

@pytest.mark.asyncio
async def test_verify_and_process_image(image_processor, tmp_path, sample_image):
    """测试图片验证和处理"""
    # 准备测试文件
    test_file = tmp_path / "test.jpg"
    with open(test_file, 'wb') as f:
        f.write(sample_image)
    
    # 测试处理
    is_valid, processed_path, error = await image_processor.verify_and_process_image(
        str(test_file),
        quality=85,
        max_width=1920,
        max_height=1080
    )
    
    assert is_valid
    assert processed_path
    assert not error
    
    # 验证处理后的图片
    processed_img = Image.open(processed_path)
    width, height = processed_img.size
    assert width <= 1920
    assert height <= 1080

@pytest.mark.asyncio
async def test_invalid_image(image_processor, tmp_path):
    """测试无效图片文件"""
    # 创建一个无效的图片文件
    test_file = tmp_path / "invalid.jpg"
    with open(test_file, 'wb') as f:
        f.write(b'not an image')
    
    # 测试处理
    is_valid, processed_path, error = await image_processor.verify_and_process_image(
        str(test_file),
        quality=85,
        max_width=1920,
        max_height=1080
    )
    
    assert not is_valid
    assert error
    assert not processed_path

@pytest.mark.asyncio
async def test_mime_type_check(image_processor, tmp_path, sample_image):
    """测试MIME类型检查"""
    # 准备测试文件
    test_file = tmp_path / "test.jpg"
    with open(test_file, 'wb') as f:
        f.write(sample_image)
    
    mime_type = await image_processor._get_mime_type(str(test_file))
    assert mime_type == 'image/jpeg'

@pytest.mark.asyncio
async def test_process_image(image_processor, tmp_path, sample_image):
    """测试图片处理功能"""
    # 准备测试文件
    test_file = tmp_path / "test.jpg"
    with open(test_file, 'wb') as f:
        f.write(sample_image)
    
    # 测试不同的处理参数
    test_cases = [
        {'quality': 85, 'max_width': 1920, 'max_height': 1080},
        {'quality': 50, 'max_width': 800, 'max_height': 600},
        {'quality': 100, 'max_width': 3840, 'max_height': 2160}
    ]
    
    for params in test_cases:
        is_valid, processed_path, error = await image_processor.verify_and_process_image(
            str(test_file),
            **params
        )
        
        assert is_valid
        assert processed_path
        assert not error
        
        # 验证处理后的图片
        processed_img = Image.open(processed_path)
        width, height = processed_img.size
        assert width <= params['max_width']
        assert height <= params['max_height']
