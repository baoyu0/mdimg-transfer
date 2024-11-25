"""性能分析模块"""

import asyncio
import cProfile
import io
import pstats
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from .collectors import ProcessingMetrics

T = TypeVar('T')

class AsyncProfiler:
    """异步性能分析器"""

    def __init__(self, enabled: bool = True):
        """
        初始化分析器

        Args:
            enabled: 是否启用分析
        """
        self.enabled = enabled
        self._profiler = cProfile.Profile()
        self._metrics = ProcessingMetrics()

    async def profile(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        分析函数性能

        Args:
            func: 要分析的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            函数返回值
        """
        if not self.enabled:
            return await func(*args, **kwargs)

        # 启动分析器
        self._profiler.enable()
        start_time = time.time()

        try:
            # 执行函数
            result = await func(*args, **kwargs)
            return result

        finally:
            # 停止分析器
            self._profiler.disable()
            duration = time.time() - start_time

            # 记录性能指标
            self._metrics.record_processing_time(duration)

    def print_stats(self, sort_by: str = 'cumulative', limit: int = 20) -> None:
        """
        打印性能统计信息

        Args:
            sort_by: 排序方式
            limit: 显示条数
        """
        if not self.enabled:
            return

        # 创建统计对象
        stream = io.StringIO()
        stats = pstats.Stats(self._profiler, stream=stream)

        # 排序并打印统计信息
        stats.sort_stats(sort_by)
        stats.print_stats(limit)

        print(stream.getvalue())

    def clear(self) -> None:
        """清除性能统计数据"""
        if self.enabled:
            self._profiler = cProfile.Profile()

def profile_async(
    name: Optional[str] = None,
    enabled: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    异步函数性能分析装饰器

    Args:
        name: 分析名称
        enabled: 是否启用分析

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        profiler = AsyncProfiler(enabled=enabled)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # 执行并分析函数
            result = await profiler.profile(func, *args, **kwargs)

            # 打印性能统计
            if enabled:
                print(f"\nPerformance profile for {name or func.__name__}:")
                profiler.print_stats()

            return result

        return wrapper
    return decorator

class PerformanceReport:
    """性能报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self._metrics = ProcessingMetrics()
        self._start_time = time.time()
        self._data = {}

    def record_metric(self, name: str, value: float) -> None:
        """
        记录性能指标

        Args:
            name: 指标名称
            value: 指标值
        """
        if name not in self._data:
            self._data[name] = []
        self._data[name].append(value)

    def generate_report(self) -> str:
        """
        生成性能报告

        Returns:
            报告内容
        """
        duration = time.time() - self._start_time

        # 构建报告
        report = ["Performance Report", "=" * 50]
        report.append(f"\nDuration: {duration:.2f}s\n")

        # 添加指标统计
        for name, values in self._data.items():
            if values:
                avg = sum(values) / len(values)
                min_val = min(values)
                max_val = max(values)
                p95 = sorted(values)[int(len(values) * 0.95)]

                report.extend([
                    f"{name}:",
                    f"  Average: {avg:.2f}",
                    f"  Min: {min_val:.2f}",
                    f"  Max: {max_val:.2f}",
                    f"  95th percentile: {p95:.2f}",
                    ""
                ])

        return "\n".join(report)

    def save_report(self, filename: str) -> None:
        """
        保存性能报告

        Args:
            filename: 文件名
        """
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)
