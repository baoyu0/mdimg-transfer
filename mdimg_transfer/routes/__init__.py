"""
路由包。
"""

from .api import bp as api
from .websocket import bp as websocket

__all__ = ['api', 'websocket']
