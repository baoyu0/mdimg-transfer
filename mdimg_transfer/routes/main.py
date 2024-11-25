"""
主路由模块。
"""

import logging
from quart import Blueprint, jsonify

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/hello')
async def hello():
    """
    测试路由。
    """
    logger.debug("Handling /hello request")
    return jsonify({
        "message": "Hello from mdimg-transfer!",
        "status": "success"
    })

@bp.route('/')
async def index():
    """
    根路由。
    """
    logger.debug("Handling / request")
    return jsonify({
        "name": "mdimg-transfer",
        "description": "Markdown image transfer tool",
        "status": "running",
        "endpoints": {
            "hello": "/api/hello",
            "upload": "/api/upload",
            "transfer": "/api/transfer"
        }
    })
