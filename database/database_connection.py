import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
db_name = os.environ.get("DATABASE_URL")


def obtain_db_connection():
    if db_name is None:
        url = parse.urlparse("pumpdetectordb")
        url_path = url.path
    else:
        url = parse.urlparse(db_name)
        url_path = url.path[1:]

    connection = psycopg2.connect(
        database=url_path,
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return connection