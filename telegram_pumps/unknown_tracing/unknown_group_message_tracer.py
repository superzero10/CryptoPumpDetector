from common.database.database_connection import obtain_db_connection

db_connection = obtain_db_connection()
db_cursor = db_connection.cursor()
db_cursor.execute('SELECT group_id, signal_type FROM pump_groups')
all_groups_list = db_cursor.fetchall()
print(all_groups_list)

db_connection.close()


def trace_unknown_group_messages(full_message):
    pass