import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse('pumpdetectordb')


def connect_to_database():
    connection = psycopg2.connect(
        database=url.path,
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    db_cursor = connection.cursor()
    db_cursor.execute('SELECT * FROM COMPANY;')
    rows = db_cursor.fetchall()
    for row in rows:
        print(" ", row[0], " ", row[1])
    return connection
