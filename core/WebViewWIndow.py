import webview
import logging
def WebViewWIndow(url: str,title: str,width: int,height: int,logger: logging.Logger):#创建Webview窗口
    webview.create_window(title=title, url=url, width=width, height=height)
    webview.settings['ALLOW_DOWNLOADS'] = True
    webview.start()
    logger.info("Webview window close.And exit.")
    exit(0)