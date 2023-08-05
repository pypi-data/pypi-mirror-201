# -*- coding:utf-8 -*-
import logging
import logging.handlers
import sys
from os import makedirs
from os.path import dirname, exists


class settings:
    # 通用配置
    LOG_ENABLED = False  # 是否开启日志
    LOG_TO_CONSOLE = True  # 是否输出到控制台
    LOG_TO_FILE = True  # 是否输出到文件
    LOG_TO_ES = False  # 是否输出到 Elasticsearch
    LOG_LEVEL = 'DEBUG'  # 日志级别: ERROR/WARNING/INFO/DEBUG
    # LOG_FORMAT = '%(levelname)s - %(asctime)s - process: %(process)d -
    # %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s'  #
    # 每条日志输出格式
    LOG_FORMAT = '[%(asctime)s][%(filename)s:%(lineno)d-%(module)s] - %(levelname)s - %(message)s'
    # 文件输出配置
    LOG_PATH = '/var/logs/runtime.log'  # 日志文件路径
    TIMED_ROTATING = True  # 日志是否按时间切割
    ROTATING_TIME = 'D'  # ,
    # ES输出日志
    ELASTIC_SEARCH_HOST = 'eshost'  # Elasticsearch Host
    ELASTIC_SEARCH_PORT = 9200  # Elasticsearch Port
    ELASTIC_SEARCH_INDEX = 'runtime'  # Elasticsearch Index Name
    APP_ENVIRONMENT = 'dev'  # 运行环境，如测试环境还是生产环境

loggers = {}


def file_logger(name=None, log_level="DEBUG", log_format=None, time_rotating='D', encoding='utf-8'):
    """
    param string name: 
    param string log_level: 日志级别: ERROR/WARNING/INFO/DEBUG
    param string log_format: 每条日志输出格式
    param string time_rotating: 日志切割时间, 可选值: S(秒)/M(分)/H(小时)/D(天)/W(周)/midnight(深夜)
    param string encoding: 编码
    """
    if not name:
        name = __name__
    logger = logging.getLogger(name)
    logger.setLevel(log_level.upper())
    if log_format is None:
        log_format = '[%(asctime)s][%(filename)s:%(lineno)d-%(module)s] - %(levelname)s - %(message)s'

    formatter = logging.Formatter(log_format)
    if time_rotating :
        file_handler = logging.handlers.TimedRotatingFileHandler(
        settings.LOG_PATH, when=time_rotating, encoding=encoding)
    else:
        file_handler = logging.FileHandler(settings.LOG_PATH, encoding=encoding)
    file_handler.setLevel(level=settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def get_logger(name=None):
    """
    get logger by name
    :param name: name of logger
    :return: logger
    """
    global loggers
    if not name:
        name = __name__
    if loggers.get(name):
        return loggers.get(name)
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    # 输出到控制台
    if settings.LOG_ENABLED and settings.LOG_TO_CONSOLE:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=settings.LOG_LEVEL)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    # 输出到文件
    if settings.LOG_ENABLED and settings.LOG_TO_FILE:
        # 如果路径不存在，创建日志文件文件夹
        log_dir = dirname(settings.LOG_PATH)
        if not exists(log_dir):
            makedirs(log_dir)
        # 添加 FileHandler
        if settings.TIMED_ROTATING:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                settings.LOG_PATH, when=settings.ROTATING_TIME, encoding='utf-8')
        else:
            file_handler = logging.FileHandler(settings.LOG_PATH, encoding='utf-8')
        file_handler.setLevel(level=settings.LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


    # 输出到 Elasticsearch
    if settings.LOG_ENABLED and settings.LOG_TO_ES:
        from cmreslogging.handlers import CMRESHandler
        # 添加 CMRESHandler
        es_handler = CMRESHandler(hosts=[{'host': settings.ELASTIC_SEARCH_HOST, 'port': settings.ELASTIC_SEARCH_PORT}],
                                  # 可以配置对应的认证权限
                                  auth_type=CMRESHandler.AuthType.NO_AUTH,
                                  es_index_name=settings.ELASTIC_SEARCH_INDEX,
                                  # 一个月分一个 Index
                                  index_name_frequency=CMRESHandler.IndexNameFrequency.MONTHLY,
                                  # 额外增加环境标识
                                  es_additional_fields={
                                      'environment': settings.APP_ENVIRONMENT}
                                  )
        es_handler.setLevel(level=settings.LOG_LEVEL)
        es_handler.setFormatter(formatter)
        logger.addHandler(es_handler)
    # 保存到全局 loggers
    loggers[name] = logger
    return logger


logger = get_logger()
if __name__ == "__main__":
    logger = get_logger()
    logger.debug("test")
    logger.warning("this is a warning message")
    logger.error("this is a error message")
    logger.info("this is a info message")
