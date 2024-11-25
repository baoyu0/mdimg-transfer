"""
启动服务器的脚本。
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
            if any('mdimg-transfer' in cmd.lower() for cmd in cmdline):
                logger.warning("发现相关进程 %s (PID: %d)", proc.name(), proc.pid)
                try:
                    # 首先尝试正常终止
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)  # 等待3秒
                    except psutil.TimeoutExpired:
                        # 如果等待超时，强制结束进程
                        logger.warning("进程未响应终止信号，正在强制结束...")
                        proc.kill()
                        proc.wait(timeout=3)
                    
                    logger.info("已终止进程 %s (PID: %d)", proc.name(), proc.pid)
                    killed = True
                except psutil.NoSuchProcess:
                    logger.info("进程已不存在")
                    killed = True
                except Exception as e:
                    logger.error("终止进程时发生错误: %s", str(e))
                    continue

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as e:
            logger.error("处理进程时发生错误: %s", str(e))
            continue

    # 然后检查并终止占用指定端口的进程
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            if proc.pid == current_pid:
                continue

            for conn in proc.connections():
                if conn.laddr.port == port:
                    logger.warning("发现端口 %d 被进程 %s (PID: %d) 占用", 
                                 port, proc.name(), proc.pid)
                    try:
                        proc.terminate()
                        try:
                            proc.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            logger.warning("进程未响应终止信号，正在强制结束...")
                            proc.kill()
                            proc.wait(timeout=3)
                        
                        logger.info("已终止进程 %s (PID: %d)", proc.name(), proc.pid)
                        killed = True
                    except psutil.NoSuchProcess:
                        logger.info("进程已不存在")
                        killed = True
                    except Exception as e:
                        logger.error("终止进程时发生错误: %s", str(e))
                        continue
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception as e:
            logger.error("处理进程时发生错误: %s", str(e))
            continue
            
    return killed

async def cleanup(hypercorn_config: Config):
    """清理资源"""
    logger.info("正在清理资源...")
    # 这里可以添加其他清理操作
    logger.info("资源清理完成")

async def handle_shutdown(hypercorn_config: Config):
    """处理关闭信号"""
    await cleanup(hypercorn_config)
    # 停止 Hypercorn
    hypercorn_config.shutdown()

def main():
    """主函数"""
    # 添加命令行参数解析
    import argparse
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
    pid_file = Path(__file__).parent / '.server.pid'
    pid_file.write_text(str(os.getpid()))

def stop_server():
    """停止服务器"""
    pid_file = Path(__file__).parent / '.server.pid'
    
    if not pid_file.exists():
        logger.warning('找不到PID文件，服务器可能没有在运行')
        # 尝试清理端口
        if kill_process_on_port(int(os.getenv('PORT', 5000))):
            logger.info('已终止占用端口的进程')
        return 0
    
    try:
        pid = int(pid_file.read_text().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info(f'已发送终止信号到进程 {pid}')
            # 等待进程结束
            for _ in range(10):  # 最多等待5秒
                try:
                    os.kill(pid, 0)  # 检查进程是否存在
                    time.sleep(0.5)
                except OSError:
                    break
            else:
                # 如果进程仍然存在，强制终止
                os.kill(pid, signal.SIGKILL)
                logger.info(f'已强制终止进程 {pid}')
        except ProcessLookupError:
            logger.warning(f'进程 {pid} 不存在')
        except PermissionError:
            logger.error(f'没有权限终止进程 {pid}')
            return 1
    except ValueError:
        logger.error('PID文件格式错误')
    finally:
        # 清理PID文件
        try:
            pid_file.unlink()
        except Exception as e:
            logger.error(f'删除PID文件时发生错误: {e}')
    
    # 确保端口被释放
    if kill_process_on_port(int(os.getenv('PORT', 5000))):
        logger.info('已释放端口')
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在退出...")
        sys.exit(0)
