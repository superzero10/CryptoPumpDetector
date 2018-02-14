from common.database.database_connection import create_db_connection


def save_session_file():
    print('saving session file')
    db_connection = create_db_connection()
    session_file_content = open('telegram.session', 'rb').read()
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM session_blob")
    db_connection.commit()
    cursor.execute("INSERT INTO session_blob(session_blob) VALUES (%s);",
                   [session_file_content])
    db_connection.commit()
    db_connection.close()


def save_phone_code_hash(hash):
    db_connection = create_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM auth_code")
    db_connection.commit()
    cursor.execute("INSERT INTO auth_code(code, launch, code_hash) VALUES (%s, %s, %s);",
                   [-1, False, hash])
    db_connection.commit()
    db_connection.close()


def fetch_auth_code_from_db():
    return __fetch_auth_data(param=0)


def is_auth_code_available():
    return __fetch_auth_data(param=1)


def fetch_phone_code_hash_from_db():
    return __fetch_auth_data(param=2)


def __fetch_auth_data(param):
    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT code, launch, code_hash FROM auth_code')
    auth_data = db_cursor.fetchall()
    db_connection.close()

    # a list containing one tuple
    if auth_data:
        return auth_data[0][param]
    else:
        return None
