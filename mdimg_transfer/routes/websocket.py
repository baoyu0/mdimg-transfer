"""
WebSocket 路由模块。
提供实时进度更新和结果通知。
"""

import logging
from quart import Blueprint, websocket, current_app
import json
import asyncio
from typing import Dict, Set

logger = logging.getLogger(__name__)

bp = Blueprint('websocket', __name__)

# 存储活动的 WebSocket 连接
active_connections: Dict[str, Set] = {}

@bp.websocket('/ws/<client_id>')
async def ws(client_id: str):
    """
    WebSocket 连接处理。
    
    Args:
        client_id: 客户端唯一标识
    """
    try:
        # 存储连接
        if client_id not in active_connections:
            active_connections[client_id] = set()
        active_connections[client_id].add(websocket._get_current_object())
        
        logger.info(f"WebSocket connected: {client_id}")
        
        while True:
            try:
                # 接收消息
                data = await websocket.receive()
                message = json.loads(data)
                
                # 处理消息
                await handle_message(client_id, message)
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_id}")
                continue
                
    except asyncio.CancelledError:
        logger.info(f"WebSocket connection cancelled: {client_id}")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
    
    finally:
        # 清理连接
        if client_id in active_connections:
            active_connections[client_id].discard(websocket._get_current_object())
            if not active_connections[client_id]:
                del active_connections[client_id]
        logger.info(f"WebSocket disconnected: {client_id}")

async def handle_message(client_id: str, message: dict):
    """
    处理接收到的 WebSocket 消息。
    
    Args:
        client_id: 客户端唯一标识
        message: 消息内容
    """
    try:
        # 根据消息类型处理
        message_type = message.get('type', 'unknown')
        
        if message_type == 'start_process':
            # 开始处理任务
            await send_progress(client_id, 0, "开始处理...")
            
            # TODO: 实现实际的处理逻辑
            
            await send_progress(client_id, 100, "处理完成")
            
        elif message_type == 'cancel':
            # 取消处理
            # TODO: 实现取消处理逻辑
            await send_message(client_id, {
                'type': 'cancelled',
                'message': '处理已取消'
            })
            
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)
        await send_error(client_id, str(e))

async def send_progress(client_id: str, progress: int, message: str = None):
    """
    发送进度更新。
    
    Args:
        client_id: 客户端唯一标识
        progress: 进度百分比 (0-100)
        message: 可选的进度消息
    """
    await send_message(client_id, {
        'type': 'progress',
        'progress': progress,
        'message': message
    })

async def send_error(client_id: str, error: str):
    """
    发送错误消息。
    
    Args:
        client_id: 客户端唯一标识
        error: 错误消息
    """
    await send_message(client_id, {
        'type': 'error',
        'error': error
    })

async def send_message(client_id: str, message: dict):
    """
    向指定客户端发送消息。
    
    Args:
        client_id: 客户端唯一标识
        message: 要发送的消息
    """
    if client_id not in active_connections:
        return
    
    # 转换为 JSON 字符串
    data = json.dumps(message)
    
    # 向客户端的所有连接发送消息
    for ws in active_connections[client_id].copy():
        try:
            await ws.send(data)
        except Exception as e:
            logger.error(f"Error sending message to {client_id}: {e}")
            active_connections[client_id].discard(ws)
