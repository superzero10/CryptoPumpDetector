from common.database.database_connection import create_db_connection
from psycopg2._json import Json
from time import time


def save_unknown_group_message(cleaned_message):
    print('Message after cleaning', cleaned_message)
    db_connection = create_db_connection()

    try:
        db_cursor = db_connection.cursor()
        db_cursor.execute('INSERT into traced_messages (timestamp, chat_id, full_message) values (%s, %s, %s)',
                          [time(), cleaned_message.to_id.channel_id, Json(cleaned_message)])
    except Exception as err:
        print(err)
    finally:
        db_connection.commit()
        db_connection.close()


def save_unlisted_group(group_id):
    pass
