# -*- coding:utf-8 -*- 
import logging
import logging.handlers


def file_logger(log_path="runtime.log", log_level="DEBUG", log_format=None, time_rotating='D', encoding='utf-8', name=None):
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
        log_format = '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d-%(module)s] %(message)s'

    formatter = logging.Formatter(log_format)
    if time_rotating:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_path, when=time_rotating, encoding=encoding)
    else:
        file_handler = logging.FileHandler(
            log_path, encoding=encoding)
    file_handler.setLevel(level=log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    logger = file_logger()
    logger.info("info")
    logger.debug("debug")