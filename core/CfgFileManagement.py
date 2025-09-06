import toml
import logging

def InitCfgFile(logger : logging.Logger) -> None:
    """
    初始化配置文件
    :return:
    """
    DEFAULT_CFG : dict = {
        'webview': {
            'enabled': True,
            'title': 'PyWebPageUI',
            'width': 1280,
            'height': 720,
            'host':"0.0.0.0",
            'port': 5000
        }
    }
    with open('./cfg/config.toml', 'w', encoding='utf-8') as file:
        toml.dump(DEFAULT_CFG, file)
    logger.info('Config file init done')
    return None

def LoadCfgFile(logger : logging.Logger) -> dict:
    """
    加载配置文件
    :return:
    """
    try:
        with open('./cfg/config.toml', 'r', encoding='utf-8') as file:
            cfg = toml.load(file)
    except FileNotFoundError:
        logger.warning('Config file not found')
        logger.info('Config file not found,init config file')
        InitCfgFile(logger)
        with open('./cfg/config.toml', 'r', encoding='utf-8') as file:
            cfg = toml.load(file)
    except toml.TomlDecodeError:
        logger.error('Config file decode error')
        logger.info("Please attempt to use the configuration file repair tool. If you are unable to fix it, seek assistance from others.")
        exit(1)
    return cfg