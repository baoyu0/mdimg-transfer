"""
监控接口路由模块。
"""

from quart import Blueprint, Response, jsonify
from ..core.metrics import metrics

bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')

@bp.route('/metrics')
async def get_metrics() -> Response:
    """
    获取 Prometheus 格式的指标数据。
    
    Returns:
        Response: Prometheus 格式的指标数据
    """
    return Response(
        metrics.get_metrics(),
        mimetype='text/plain; version=0.0.4'
    )

@bp.route('/stats')
async def get_stats():
    """
    获取统计信息。
    
    Returns:
        dict: 包含各项统计数据的字典
    """
    return jsonify(metrics.get_stats())
