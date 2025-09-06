import os
import sys
import importlib
import platform
def EnvironmentCheck() -> bool:
    """
    检查环境是否符合要求
    :return:
    """
    LIB_LIST : list[str] = ['flask','toml']
    if sys.version_info < (3, 9):
        return False
    for lib in LIB_LIST:
        if importlib.util.find_spec(lib) is None:
            return False
    return True

def CheckWebviewInstalled() -> tuple[bool,str]:
    """
    检查WebView框架是否已安装
    :return:
    """
    system_platform : str = platform.system()

    if system_platform == "Windows":
        # 检查WebView2
        webview2_path : str = r'C:\Program Files (x86)\Microsoft\EdgeWebView2'
        webview2_dll : str = '\WebView2Loader.dll'
        for root, dirs, files in os.walk(webview2_path):
            if webview2_dll in files:
                return (True,'')
        return (False,"No installed WebView2")

    elif system_platform == "Darwin":
        # 检查WebKit框架
        webkit_path = '/System/Library/Frameworks/WebKit.framework'
        if os.path.exists(webkit_path):
            return (True,'')
        return (False,"Unsupported WKWebView")

    elif system_platform == "Linux":
        # 检查WebKitGTK
        webkitgtk_paths = [
            '/usr/lib/libwebkit2gtk-4.0.so',
            '/usr/lib/x86_64-linux-gnu/libwebkit2gtk-4.0.so'
        ]
        for path in webkitgtk_paths:
            if os.path.exists(path):
                return (True,'')
        
        # 检查QtWebEngine
        qtwebengine_paths = [
            '/usr/lib/qt5/bin/qtwebengine_process',
            '/usr/lib/x86_64-linux-gnu/qt5/bin/qtwebengine_process'
        ]
        for path in qtwebengine_paths:
            if os.path.exists(path):
                return "QtWebEngine已安装"
        
        return (False,"Not Found Webview framework.")

    else:
        return (False,"Unsupported OS.")

def CheckPortAvailable(port : int) -> bool:
    """
    检查端口是否可用
    :param port:
    :return:
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0
    return False