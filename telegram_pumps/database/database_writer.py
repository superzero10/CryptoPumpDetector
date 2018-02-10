from common.database.database_connection import create_db_connection
from psycopg2._json import Json
from time import time


def save_unknown_group_message(full_message):
    message_dict = full_message.to_dict(recursive=True)

    keys_to_remove = ['fwd_from', 'date', 'to_id', 'media_unread', 'out', 'mentioned', 'via_bot_id', 'reply_to_msg_id',
                      'id', 'edit_date', 'post_author', 'views']
    for key in keys_to_remove:
        message_dict.pop(key, None)

    print('Message after cleaning', message_dict)

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('INSERT into traced_messages (timestamp, chat_id, full_message) values (%s, %s, %s)',
                          [time(), full_message.to_id.channel_id, Json(message_dict)])
    except Exception as err:
        print(err)
    finally:
        db_connection.commit()
        db_connection.close()
