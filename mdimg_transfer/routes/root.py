"""
根路由模块。
"""

import logging
import os
from quart import Blueprint, render_template, jsonify, current_app

logger = logging.getLogger(__name__)

# 创建蓝图时指定 url_prefix
bp = Blueprint('root', __name__, url_prefix='')

@bp.route('/')
async def index():
    """
    根路由，返回主页面。
    """
    logger.debug("Handling index request")
    try:
        logger.debug("Attempting to render template")
        template = await render_template('index.html')
        logger.debug("Template rendered successfully")
        return template
    except Exception as e:
        logger.error(f"Error rendering template: {e}", exc_info=True)
        return jsonify({
            "error": "Template rendering failed",
            "message": str(e),
            "type": str(type(e))
        }), 500

@bp.route('/test')
async def test():
    """
    测试路由
    """
    logger.debug("Handling test request")
    return jsonify({
        "status": "ok",
        "message": "Test route works!"
    })

@bp.route('/api/info')
async def api_info():
    """
    API信息端点，返回应用状态和版本信息。
    """
    logger.debug("Handling API info request")
    return jsonify({
        "name": "mdimg-transfer",
        "description": "Markdown image transfer tool",
        "status": "running",
        "version": "1.0.0"
    })
