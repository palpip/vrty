import logging
import datetime as dt
from _settings import *

def create_logger(logname):
    '''Create and return a logger with the specified name'''
    logger = logging.getLogger(logname)
    logger.addHandler(logging.FileHandler(TOPDIR + f"{dt.datetime.now().strftime('%H-%M')}-{logname}.log", mode='w'))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def print_log_error(logger, msg):
    print(msg)
    logger.error(msg)