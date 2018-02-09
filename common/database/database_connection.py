import os
import urllib.parse as urlparse
from urllib import parse

import psycopg2

parse.uses_netloc.append('postgres')
db_name = os.environ.get('DATABASE_URL')


def create_db_connection():
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:] if url.path != 'pumpdetectordb' else url.path
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    return connection


create_db_connection()
