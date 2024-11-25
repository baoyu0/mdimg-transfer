"""WebSocket处理模块"""

import asyncio
import json
from typing import Dict, Set
from quart import Websocket

class ConnectionManager:
    """WebSocket连接管理器"""
    def __init__(self):
        self.active_connections: Dict[str, Websocket] = {}
        self.tasks: Dict[str, Set[str]] = {}  # task_id -> set of client_ids

    async def connect(self, ws: Websocket, client_id: str):
        """建立WebSocket连接"""
        self.active_connections[client_id] = ws

    def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        # 清理任务关联
        for task_id in list(self.tasks.keys()):
            if client_id in self.tasks[task_id]:
                self.tasks[task_id].remove(client_id)
            if not self.tasks[task_id]:
                del self.tasks[task_id]

    async def send_progress(self, client_id: str, data: dict):
        """发送进度信息"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(data)
            except Exception:
                self.disconnect(client_id)

    async def broadcast_progress(self, task_id: str, data: dict):
        """广播进度信息到所有关联的客户端"""
        if task_id in self.tasks:
            for client_id in self.tasks[task_id]:
                await self.send_progress(client_id, data)

    def register_task(self, task_id: str, client_id: str):
        """注册任务与客户端的关联"""
        if task_id not in self.tasks:
            self.tasks[task_id] = set()
        self.tasks[task_id].add(client_id)

manager = ConnectionManager()
