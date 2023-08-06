from nsj_multi_database_lib.settings import MULTI_DATABASE_HOST
from nsj_multi_database_lib.settings import MULTI_DATABASE_PASS
from nsj_multi_database_lib.settings import MULTI_DATABASE_PORT
from nsj_multi_database_lib.settings import MULTI_DATABASE_NAME
from nsj_multi_database_lib.settings import MULTI_DATABASE_USER
from nsj_multi_database_lib.settings import DEFAULT_EXTERNAL_DATABASE_USER
from nsj_multi_database_lib.settings import DEFAULT_EXTERNAL_DATABASE_PASSWORD
from flask import g

import sqlalchemy


def create_pool(database_conn_url):
    # Creating database connection pool
    db_pool = sqlalchemy.create_engine(
        database_conn_url,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
        # TODO: verificar se client_encoding aqui é necessário, pois segundo este link:
        # https://stackoverflow.com/questions/14783505/encoding-error-with-sqlalchemy-and-postgresql
        # o sqlalchemy usa, por padrão, o encoding da configuração do banco de dados 
        # , client_encoding='utf8'
    )
    return db_pool

def create_external_pool_with_default_credentials():
    external_database = g.external_database
    external_database_conn_url = f'postgresql+pg8000://{DEFAULT_EXTERNAL_DATABASE_USER}:{DEFAULT_EXTERNAL_DATABASE_PASSWORD}@{external_database["host"]}:{external_database["port"]}/{external_database["name"]}'
    external_db_pool = create_pool(external_database_conn_url)
    return external_db_pool

def create_external_pool():
    external_database = g.external_database
    external_database_conn_url = f'postgresql+pg8000://{external_database["user"]}:{external_database["password"]}@{external_database["host"]}:{external_database["port"]}/{external_database["name"]}'
    external_db_pool = create_pool(external_database_conn_url)
    return external_db_pool


internal_database_conn_url = f'postgresql+pg8000://{MULTI_DATABASE_USER}:{MULTI_DATABASE_PASS}@{MULTI_DATABASE_HOST}:{MULTI_DATABASE_PORT}/{MULTI_DATABASE_NAME}'
internal_db_pool = create_pool(internal_database_conn_url)

