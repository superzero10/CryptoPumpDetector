from common.database.database_connection import create_db_connection

chat_id = input('Input chat ID:')

db_connection = create_db_connection()
db_cursor = db_connection.cursor()
db_cursor.execute('SELECT full_message FROM coins WHERE chat_id = %s', chat_id)
rows = db_cursor.fetchall()
print(rows)
db_connection.close()
