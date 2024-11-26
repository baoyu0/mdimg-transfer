"""
文件处理服务。
提供Markdown文件处理、图片下载和上传功能。
支持断点续传、并发处理和错误恢复。
"""

import os
import re
import json
import aiohttp
import aiofiles
import asyncio
import logging
import hashlib
from typing import Callable, Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from werkzeug.datastructures import FileStorage
from ..config import Config
from ..utils.r2_client import R2Client

logger = logging.getLogger(__name__)

@dataclass
class ImageTask:
    """图片处理任务"""
    url: str
    index: int
    local_filename: str
    r2_key: str
    status: str = 'pending'  # pending, downloading, uploading, completed, error
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    checksum: Optional[str] = None

class FileProcessor:
    """文件处理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.r2_client = R2Client()
        self.processed_dir = Path('processed')
        self.images_dir = self.processed_dir / 'images'
        self.state_dir = self.processed_dir / 'state'
        self._setup_directories()
        
    def _setup_directories(self):
        """创建必要的目录"""
        for directory in [self.processed_dir, self.images_dir, self.state_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _create_state_file(self, task_id: str) -> Path:
        """创建状态文件路径"""
        return self.state_dir / f"{task_id}_state.json"
        
    def _save_state(self, task_id: str, content: str, image_tasks: List[ImageTask]):
        """保存处理状态"""
        state = {
            'content': content,
            'image_tasks': [vars(task) for task in image_tasks],
            'timestamp': datetime.now().isoformat()
        }
        state_file = self._create_state_file(task_id)
        with state_file.open('w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            
    def _load_state(self, task_id: str) -> Tuple[Optional[str], List[ImageTask]]:
        """加载处理状态"""
        state_file = self._create_state_file(task_id)
        if not state_file.exists():
            return None, []
            
        try:
            with state_file.open('r', encoding='utf-8') as f:
                state = json.load(f)
            image_tasks = [ImageTask(**task) for task in state['image_tasks']]
            return state['content'], image_tasks
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            return None, []
            
    async def _download_image(self, session: aiohttp.ClientSession, task: ImageTask) -> bool:
        """下载单个图片"""
        try:
            task.status = 'downloading'
            local_path = self.images_dir / task.local_filename
            
            # 如果文件已存在且校验和匹配，跳过下载
            if local_path.exists() and task.checksum:
                with local_path.open('rb') as f:
                    current_checksum = hashlib.md5(f.read()).hexdigest()
                if current_checksum == task.checksum:
                    task.status = 'completed'
                    return True
            
            async with session.get(task.url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # 获取和验证内容类型
                    content_type = response.headers.get('content-type', '').lower()
                    if not any(ext in content_type for ext in ['jpeg', 'jpg', 'png', 'gif', 'webp']):
                        raise ValueError(f"Unsupported image type: {content_type}")
                    
                    # 保存图片和元数据
                    task.content_type = content_type
                    task.file_size = len(image_data)
                    task.checksum = hashlib.md5(image_data).hexdigest()
                    
                    with local_path.open('wb') as f:
                        f.write(image_data)
                    
                    return True
                else:
                    raise ValueError(f"HTTP {response.status}: {response.reason}")
                    
        except Exception as e:
            task.error = str(e)
            logger.error(f"Error downloading image {task.url}: {e}")
            return False
            
    async def _upload_to_r2(self, task: ImageTask) -> Optional[str]:
        """上传图片到R2"""
        try:
            task.status = 'uploading'
            local_path = self.images_dir / task.local_filename
            if not local_path.exists():
                raise FileNotFoundError(f"Image file not found: {local_path}")
                
            r2_url = await self.r2_client.upload_file(str(local_path), task.r2_key)
            task.status = 'completed'
            return r2_url
            
        except Exception as e:
            task.error = str(e)
            logger.error(f"Error uploading image {task.local_filename}: {e}")
            return None
            
    async def _process_image_task(self, session: aiohttp.ClientSession, task: ImageTask,
                               semaphore: asyncio.Semaphore) -> Optional[str]:
        """处理单个图片任务"""
        while True:
            try:
                async with semaphore:
                    # 下载图片
                    if task.status == 'pending' or task.status == 'error':
                        task.status = 'downloading'
                        if not await self._download_image(session, task):
                            task.status = 'error'
                            break
                    
                    # 上传到R2
                    if task.status == 'downloading':
                        task.status = 'uploading'
                        if not await self._upload_to_r2(task):
                            task.status = 'error'
                            break
                        task.status = 'completed'
                        return task
                    
                if task.retries < task.max_retries:
                    task.retries += 1
                    await asyncio.sleep(1 * task.retries)  # 指数退避
                else:
                    break
                    
            except Exception as e:
                task.error = str(e)
                logger.error(f"Error processing image {task.url}: {e}")
                if task.retries >= task.max_retries:
                    break
                task.retries += 1
                await asyncio.sleep(1 * task.retries)
                
        return None

    async def process_markdown_file(self, file: FileStorage, task_id: str,
                                progress_callback: Callable = None,
                                max_concurrent: int = 5) -> Dict[str, Any]:
        """处理Markdown文件，下载图片并上传到R2"""
        try:
            # 读取文件内容
            content = file.read().decode('utf-8')
            file.seek(0)
            
            # 从之前的状态恢复
            saved_content, saved_tasks = self._load_state(task_id)
            if saved_content and saved_tasks:
                content = saved_content
                image_tasks = saved_tasks
                logger.info(f"Restored state for task {task_id}")
            else:
                # 查找所有图片链接并创建任务
                image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)
                image_tasks = []
                for i, url in enumerate(image_urls, 1):
                    ext = url.split('.')[-1].lower()
                    if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                        ext = 'jpg'
                    local_filename = f'image_{i}.{ext}'
                    r2_key = f'images/{task_id}/{local_filename}'
                    image_tasks.append(ImageTask(
                        url=url,
                        index=i,
                        local_filename=local_filename,
                        r2_key=r2_key
                    ))
            
            total_images = len(image_tasks)
            if total_images == 0:
                return {
                    'download_url': None,
                    'total_images': 0,
                    'successful_downloads': 0
                }
            
            # 创建信号量限制并发下载
            semaphore = asyncio.Semaphore(max_concurrent)
            
            # 更新初始进度
            if progress_callback:
                progress_callback({
                    'message': f'开始处理 {total_images} 张图片...',
                    'progress': 0,
                    'details': {
                        'total': total_images,
                        'current': 0,
                        'success': 0,
                        'failed': 0
                    }
                })
            
            # 保存初始状态
            self._save_state(task_id, content, image_tasks)
            
            # 创建HTTP会话
            async with aiohttp.ClientSession() as session:
                # 并发处理所有图片
                tasks = [
                    self._process_image_task(session, task, semaphore)
                    for task in image_tasks
                ]
                completed_tasks = await asyncio.gather(*tasks)
            
            # 统计处理结果
            successful = [task for task in completed_tasks if task and task.status == 'completed']
            successful_count = len(successful)
            
            # 替换图片链接
            for task in successful:
                old_link = f'({task.url})'
                new_link = f'({self.config.R2_PUBLIC_URL}/{task.r2_key})'
                content = content.replace(old_link, new_link)
            
            # 保存处理后的文件
            output_filename = f'{task_id}.md'
            output_path = self.processed_dir / output_filename
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            # 清理状态文件
            state_file = self._create_state_file(task_id)
            if state_file.exists():
                state_file.unlink()
            
            return {
                'download_url': f'/download/{output_filename}',
                'total_images': total_images,
                'successful_downloads': successful_count
            }
            
        except Exception as e:
            logger.error(f"Error processing markdown file: {e}")
            raise
