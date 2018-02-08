from common.database.database_connection import obtain_db_connection


def is_auth_code_available():
    __fetch_auth_data(False)


def obtain_auth_code_from_db():
    __fetch_auth_data(True)


def __fetch_auth_data(auth_code_requested):
    db_connection = obtain_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT code, launch FROM auth_code')
    auth_data = db_cursor.fetchall()
    db_connection.close()

    if auth_code_requested:
        return auth_data[0]
    else:
        return auth_data[1]
