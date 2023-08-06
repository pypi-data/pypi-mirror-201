import logging
import os


def get_logger():
    APP_NAME = os.getenv('APP_NAME', 'nsj_multi_database_lib')
    return logging.getLogger(APP_NAME)
