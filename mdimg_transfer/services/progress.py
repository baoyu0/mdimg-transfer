"""
进度管理服务。
提供任务进度跟踪、状态管理和历史记录功能。
"""

import uuid
import time
import json
import logging
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    ERROR = 'error'
    CANCELLED = 'cancelled'

class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3

@dataclass
class TaskHistory:
    """任务历史记录"""
    timestamp: float
    status: TaskStatus
    message: str
    progress: int
    details: Dict[str, Any]

@dataclass
class Progress:
    """任务进度信息"""
    task_id: str
    status: TaskStatus
    message: str
    progress: int  # 0-100
    details: Dict[str, Any]
    timestamp: float
    priority: TaskPriority
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    history: List[TaskHistory] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
        if isinstance(self.priority, int):
            self.priority = TaskPriority(self.priority)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        data = asdict(self)
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        return data

    def add_history(self, message: str, progress: int = None, details: Dict[str, Any] = None):
        """添加历史记录"""
        history_entry = TaskHistory(
            timestamp=time.time(),
            status=self.status,
            message=message,
            progress=progress if progress is not None else self.progress,
            details=details if details is not None else {}
        )
        self.history.append(history_entry)

class ProgressManager:
    """进度管理器"""
    
    def __init__(self, history_dir: str = None):
        self._tasks: Dict[str, Progress] = {}
        self._history_dir = Path(history_dir) if history_dir else None
        if self._history_dir:
            self._history_dir.mkdir(parents=True, exist_ok=True)
            
    def create_task(self, priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """创建新任务并返回任务ID"""
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = Progress(
            task_id=task_id,
            status=TaskStatus.PENDING,
            message='Task created',
            progress=0,
            details={},
            timestamp=time.time(),
            priority=priority
        )
        return task_id
        
    def update_progress(self, task_id: str, message: str, progress: int = None, 
                       details: Dict[str, Any] = None, save_history: bool = True):
        """更新任务进度"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        if task.status in [TaskStatus.COMPLETED, TaskStatus.ERROR, TaskStatus.CANCELLED]:
            return
            
        task.status = TaskStatus.PROCESSING
        task.message = message
        if progress is not None:
            task.progress = progress
        if details:
            task.details.update(details)
        task.timestamp = time.time()
        
        if save_history:
            task.add_history(message, progress, details)
        
    def set_completed(self, task_id: str, details: Dict[str, Any] = None):
        """标记任务为完成"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.progress = 100
        task.message = 'Task completed'
        task.end_time = time.time()
        if details:
            task.details.update(details)
        task.add_history('Task completed', 100, details)
        
        self._save_task_history(task)
        
    def set_error(self, task_id: str, error_message: str, details: Dict[str, Any] = None,
                  retry: bool = True):
        """标记任务为错误"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        if retry and task.retry_count < task.max_retries:
            task.retry_count += 1
            task.status = TaskStatus.PENDING
            task.message = f'Retrying ({task.retry_count}/{task.max_retries}): {error_message}'
            task.add_history(f'Error (retry {task.retry_count}): {error_message}', task.progress, details)
        else:
            task.status = TaskStatus.ERROR
            task.message = error_message
            task.end_time = time.time()
            if details:
                task.details.update(details)
            task.add_history('Task failed: ' + error_message, task.progress, details)
            self._save_task_history(task)
            
    def pause_task(self, task_id: str):
        """暂停任务"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        if task.status == TaskStatus.PROCESSING:
            task.status = TaskStatus.PAUSED
            task.add_history('Task paused', task.progress)
            
    def resume_task(self, task_id: str):
        """恢复任务"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        if task.status == TaskStatus.PAUSED:
            task.status = TaskStatus.PROCESSING
            task.add_history('Task resumed', task.progress)
            
    def cancel_task(self, task_id: str):
        """取消任务"""
        if task_id not in self._tasks:
            return
            
        task = self._tasks[task_id]
        task.status = TaskStatus.CANCELLED
        task.end_time = time.time()
        task.add_history('Task cancelled', task.progress)
        self._save_task_history(task)
            
    def get_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务进度"""
        if task_id not in self._tasks:
            return None
        return self._tasks[task_id].to_dict()
        
    def get_task_history(self, task_id: str) -> List[Dict[str, Any]]:
        """获取任务历史记录"""
        if task_id not in self._tasks:
            return []
        return [asdict(h) for h in self._tasks[task_id].history]
        
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """获取所有活动任务"""
        active_tasks = []
        for task in self._tasks.values():
            if task.status in [TaskStatus.PENDING, TaskStatus.PROCESSING, TaskStatus.PAUSED]:
                active_tasks.append(task.to_dict())
        return sorted(active_tasks, key=lambda x: (x['priority'], x['timestamp']), reverse=True)
        
    def cleanup_old_tasks(self, max_age_seconds: int = 3600):
        """清理旧任务"""
        current_time = time.time()
        to_remove = []
        for task_id, task in self._tasks.items():
            if task.status in [TaskStatus.COMPLETED, TaskStatus.ERROR, TaskStatus.CANCELLED]:
                if current_time - task.timestamp > max_age_seconds:
                    to_remove.append(task_id)
                    
        for task_id in to_remove:
            task = self._tasks[task_id]
            self._save_task_history(task)
            del self._tasks[task_id]
            
    def _save_task_history(self, task: Progress):
        """保存任务历史到文件"""
        if not self._history_dir:
            return
            
        history_file = self._history_dir / f"{task.task_id}_{datetime.fromtimestamp(task.timestamp).strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with history_file.open('w', encoding='utf-8') as f:
                json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving task history: {e}")
