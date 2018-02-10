from common.database.database_connection import create_db_connection


def is_auth_code_available():
    return __fetch_auth_data(False)


def fetch_auth_code_from_db():
    return __fetch_auth_data(True)


def __fetch_auth_data(auth_code_requested):
    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT code, launch FROM auth_code')
    auth_data = db_cursor.fetchall()
    db_connection.close()

    if auth_code_requested:
        # a list containing one tuple
        return auth_data[0][0]
    else:
        return auth_data[0][1]
