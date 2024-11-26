"""
服务器控制脚本。
"""
import os
import sys
import logging
import asyncio
import signal
import psutil
import socket
from pathlib import Path
from dotenv import load_dotenv
from hypercorn.config import Config
from hypercorn.asyncio import serve
from mdimg_transfer.create_app import create_app
from mdimg_transfer.config import config as app_config
import argparse
import time

# 加载环境变量
load_dotenv()

# 配置日志
logger = logging.getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def kill_process_on_port(port: int) -> bool:
    """终止占用指定端口的进程"""
    killed = False
    current_pid = os.getpid()  # 获取当前进程ID

    # 首先终止所有相关的Python进程（除了当前进程）
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # 检查是否是Python进程
            if proc.name().lower() not in ['python.exe', 'pythonw.exe']:
                continue
            
            # 跳过当前进程
            if proc.pid == current_pid:
                continue

            # 检查命令行参数，确保是我们的应用相关进程
            cmdline = proc.cmdline()
            if not any('start_server.py' in arg.lower() for arg in cmdline):
                continue

            # 终止进程
            proc.terminate()
            killed = True
            logger.info(f'已终止进程 {proc.pid}')

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return killed

async def cleanup(hypercorn_config: Config):
    """清理资源"""
    await hypercorn_config.shutdown()

async def handle_shutdown(hypercorn_config: Config):
    """处理关闭信号"""
    await cleanup(hypercorn_config)

def main():
    """主函数"""
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='MDImg Transfer 服务器管理')
    parser.add_argument('action', choices=['start', 'stop'], nargs='?', default='start',
                       help='执行的操作: start - 启动服务器, stop - 停止服务器')
    args = parser.parse_args()

    if args.action == 'stop':
        return stop_server()
    
    # 启动服务器的逻辑
    port = int(os.getenv('PORT', 5000))
    
    # 检查端口占用
    if is_port_in_use(port):
        logger.warning(f'发现端口 {port} 被占用')
        if not kill_process_on_port(port):
            logger.error(f'无法释放端口 {port}，请手动终止占用该端口的进程')
            return 1
        logger.info(f'已释放端口 {port}')
    
    try:
        # 创建应用实例
        app = create_app()
        
        # 配置 Hypercorn
        hypercorn_config = Config()
        hypercorn_config.bind = [f'127.0.0.1:{port}']
        
        # 在Windows上不使用信号处理器
        if os.name != 'nt':
            # 注册信号处理
            for signal_type in (signal.SIGINT, signal.SIGTERM):
                asyncio.get_event_loop().add_signal_handler(
                    signal_type, 
                    lambda: asyncio.create_task(handle_shutdown(hypercorn_config))
                )
        
        # 保存PID到文件
        save_pid()
        
        # 启动服务器
        logger.info(f'正在启动服务器，监听端口: {port}')
        return asyncio.run(serve(app, hypercorn_config))
    
    except Exception as e:
        logger.error(f'启动服务器时发生错误: {e}')
        return 1

def save_pid():
    """保存当前进程PID到文件"""
    pid = os.getpid()
    with open('.server.pid', 'w') as f:
        f.write(str(pid))

def stop_server():
    """停止服务器"""
    try:
        # 尝试从PID文件中读取进程ID
        with open('.server.pid', 'r') as f:
            pid = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        pid = None

    if pid:
        try:
            # 尝试终止进程
            process = psutil.Process(pid)
            process.terminate()
            logger.info(f'已发送终止信号到进程 {pid}')
            
            # 等待进程结束
            try:
                process.wait(timeout=5)
                logger.info('服务器已停止')
            except psutil.TimeoutExpired:
                logger.warning('服务器停止超时，尝试强制终止')
                process.kill()
                logger.info('服务器已强制停止')
            
            # 删除PID文件
            try:
                os.remove('.server.pid')
            except FileNotFoundError:
                pass
                
            return 0
            
        except psutil.NoSuchProcess:
            logger.warning(f'进程 {pid} 不存在')
        except psutil.AccessDenied:
            logger.error(f'无权限终止进程 {pid}')
            return 1
    
    # 如果没有找到PID文件或进程不存在，尝试通过端口号查找和终止进程
    port = int(os.getenv('PORT', 5000))
    if kill_process_on_port(port):
        logger.info('服务器已停止')
        return 0
    else:
        logger.warning('未找到运行中的服务器进程')
        return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info('收到中断信号，正在退出...')
        sys.exit(0)
