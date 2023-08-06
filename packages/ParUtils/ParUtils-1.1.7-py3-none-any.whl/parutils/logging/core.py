from functools import wraps

from . import g
from .logger import Logger
from parutils.file import save_list


def get_logger() -> Logger:

    if g.cur_logger is None:
        logger = Logger(file_write=False)
        g.cur_logger = logger
    else:
        logger = g.cur_logger
    return logger


def set_logger(logger):

    g.cur_logger = logger


def close_logger():

    if g.cur_logger:
        g.cur_logger.close()


def logger_methode(func):

    @wraps(func)
    def new(*args, **kwargs):
        logger = get_logger()
        logger_methode = getattr(logger, func.__name__)
        return logger_methode(*args, **kwargs)

    return new


def get_logs():
    return get_logger().logs


def update_logs(logs):
    logger = get_logger()
    logger.logs = logs
    save_list(logs + [''], logger.log_path)
