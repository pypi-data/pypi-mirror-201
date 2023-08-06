import logging
import os


MULTI_DATABASE_HOST = os.environ['MULTI_DATABASE_HOST']
MULTI_DATABASE_PASS = os.environ['MULTI_DATABASE_PASS']
MULTI_DATABASE_PORT = os.environ['MULTI_DATABASE_PORT']
MULTI_DATABASE_NAME = os.environ['MULTI_DATABASE_NAME']
MULTI_DATABASE_USER = os.environ['MULTI_DATABASE_USER']
DEFAULT_EXTERNAL_DATABASE_USER = os.environ['DEFAULT_EXTERNAL_DATABASE_USER']
DEFAULT_EXTERNAL_DATABASE_PASSWORD = os.environ['DEFAULT_EXTERNAL_DATABASE_PASSWORD']


def get_logger():
    APP_NAME = os.getenv('APP_NAME', 'nsj_multi_database_lib')
    return logging.getLogger(APP_NAME)

def get_crypt_key():
    if CRYPT_KEY is None:
        raise Exception('Faltando chave de criptografia')
    
    return CRYPT_KEY.encode()

CRYPT_KEY = os.getenv('CRYPT_KEY', None)
if CRYPT_KEY is None:
    get_logger().warning('Faltando chave de criptografia na variável de ambiente: CRYPT_KEY')
