from common.database.database_connection import create_db_connection
from psycopg2._json import Json
from time import time

keys_to_remove = ['fwd_from', 'date', 'to_id', 'media_unread', 'out', 'mentioned', 'via_bot_id', 'reply_to_msg_id',
                  'id', 'edit_date', 'post_author', 'views', 'from_id', 'entities', 'bytes']


def save_unknown_group_message(cleaned_message):
    message_dict = cleaned_message.to_dict(recursive=True)

    db_connection = create_db_connection()

    try:
        cleaned_message_dict = _clean_message(message_dict)
        print('Message after cleaning', cleaned_message_dict, '\n')

        db_cursor = db_connection.cursor()
        db_cursor.execute('INSERT into traced_messages (timestamp, chat_id, full_message) values (%s, %s, %s)',
                          [time(), cleaned_message.to_id.channel_id, Json(cleaned_message_dict)])
    except Exception as err:
        print(err)
    finally:
        db_connection.commit()
        db_connection.close()


def _clean_message(message_dict):
    if not isinstance(message_dict, dict):
        return message_dict
    return {key: value for key, value in ((key, _clean_message(value)) for key, value in message_dict.items()) if
            key not in keys_to_remove}


def save_unlisted_group(group_id):
    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT into pump_groups (group_id, name, signal_type) values (%s, %s, %s)',
                      [group_id, 'ADDED USING BOT', 'unknown'])
    db_connection.commit()
    db_connection.close()
