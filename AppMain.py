import logging
import os
from datetime import datetime
import threading
import traceback
import signal
import time
import core.CfgFileManagement as CfgFileManagement
import core.WebApp as WebApp
import core.PyWebPageAPI as PyWebPageAPI
import core.WebViewWIndow as WebViewWIndow

# 初始化设置
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 切换到当前目录

# 日志配置
def setup_logging():
    """配置日志系统"""
    if not os.path.exists('log'):
        os.makedirs('log')
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(filename)s - [%(levelname)s]: %(message)s')
    
    # 文件处理器
    log_file = f'log/{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def exit_handler(signum, frame):
    """处理退出信号"""
    logger.info('Received SIGINT signal, shutting down...')
    exit(0)

def find_available_port(start_port=5000, end_port=10000):
    """查找可用端口"""
    for port in range(start_port, end_port):
        if PyWebPageAPI.CheckPortAvailable(port):
            logger.info(f'Port {port} is available')
            return port
    logger.error('No available port found')
    exit(1)

def main():
    """主程序逻辑"""
    signal.signal(signal.SIGINT, exit_handler)
    logger.info('Welcome to PyWebPageUIBuildTool')
    
    try:
        # 环境检查
        logger.info('Check environment')
        if not PyWebPageAPI.EnvironmentCheck():
            logger.error('Environment check failed')
            exit(1)
        logger.info('Environment check passed')
        
        # Webview检查
        webview_check = PyWebPageAPI.CheckWebviewInstalled()
        if not webview_check[0]:
            logger.warning(f'{webview_check[1]}\nWebview check failed. You can continue to use the tool, '
                         'but the webview feature will not be available.')
        else:
            logger.info('Webview check passed')
        
        # 加载配置
        logger.info('Load config file')
        cfg = CfgFileManagement.LoadCfgFile(logger)
        cfg['webview']['port'] = find_available_port()
        
        # 启动应用
        app_thread = threading.Thread(
            target=WebApp.AppStart,
            args=(cfg['webview']['host'], cfg['webview']['port']),
            daemon=True
        )
        app_thread.start()
        
        try:
            WebViewWIndow.WebViewWIndow(
                f'http://127.0.0.1:{cfg["webview"]["port"]}',
                cfg['webview']['title'],
                cfg['webview']['width'],
                cfg['webview']['height'],
                logger
            )
        except Exception as e:
            logger.exception(e)
            traceback.print_exc()
            exit(1)
            
        while app_thread.is_alive():
            time.sleep(0.1)
            
        logger.info('App Exit.')
        
    except Exception as e:
        logger.exception(e)
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    logger = setup_logging()
    main()
