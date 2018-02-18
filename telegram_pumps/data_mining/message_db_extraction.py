from common.database.database_connection import create_db_connection

chat_id = input('Input chat ID:')
chat_name = input('Input chat name:')

db_connection = create_db_connection()
db_cursor = db_connection.cursor()
db_cursor.execute('SELECT full_message FROM traced_messages WHERE chat_id = %s', [chat_id])
rows = db_cursor.fetchall()

print(rows)
chat_signal_type = input('Input chat signal type:')

db_cursor.execute('DELETE FROM traced_messages WHERE chat_id = %s', [chat_id])
db_cursor.execute('DELETE FROM pump_groups WHERE group_id = %s', [chat_id])

db_cursor.execute('INSERT INTO pump_groups (group_id, name, signal_type) VALUES (%s, %s, %s)', [chat_id, chat_name, chat_signal_type])

db_connection.commit()
db_connection.close()
