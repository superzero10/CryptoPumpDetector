import os
from urllib import parse
import psycopg2

parse.uses_netloc.append('postgres')
db_name = os.environ.get('DATABASE_URL')


def create_db_connection():
    if db_name is None:
        url = parse.urlparse('pumpdetectordb')
        url_path = url.path
    else:
        url = parse.urlparse('postgres-triangular-82542')
        url_path = url.path

    print(url_path)
    connection = psycopg2.connect(
        database=url_path,
        user=url.username,
        password=url.password,
        host="/tmp/",
        port=url.port
    )

    return connection
