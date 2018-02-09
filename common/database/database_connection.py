import os
from urllib import parse
import psycopg2
from psycopg2._psycopg import OperationalError
import urllib.parse as urlparse


parse.uses_netloc.append('postgres')
db_name = os.environ.get('DATABASE_URL')


def create_db_connection():
    # if db_name is None:
    #     url = parse.urlparse('pumpdetectordb')
    #     url_path = url.path
    # else:
    #     url = parse.urlparse('postgres-triangular-82542')
    #     url_path = url.path
    #
    # print(url_path)
    #
    # try:
    #     connection = psycopg2.connect(
    #         database=url_path,
    #         user=url.username,
    #         password=url.password,
    #         host=url.hostname,
    #         port=url.port
    #     )
    # except OperationalError:
    #     connection = psycopg2.connect(
    #         database=url_path,
    #         user=url.username,
    #         password=url.password,
    #         host="/tmp",
    #         port=url.port
    #     )

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    con = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    return con

create_db_connection()