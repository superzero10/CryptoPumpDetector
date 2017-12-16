import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
db_name = os.environ.get("DATABASE_URL")


def connect_to_database():
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

    db_cursor = connection.cursor()
    db_cursor.execute('SELECT * FROM COMPANY;')
    rows = db_cursor.fetchall()
    for row in rows:
        print(row[0], row[1], )
    return connection
