from common.database.database_connection import create_db_connection


# get YoBit coins paired with BTC
def fetch_all_yobit_coins(fresh_state_needed):
    coins_list = []

    if fresh_state_needed:
        db_connection = create_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT coins_list FROM coins WHERE exchange = %s', ['yobit'])
        coins_list = db_cursor.fetchone()[0]
        db_connection.close()
    else:
        if not _yobit_coins_list:
            coins_list = fetch_all_yobit_coins(True)
        else:
            coins_list = _yobit_coins_list

    return coins_list


def fetch_all_cryptopia_coins(fresh_state_needed):
    coins_list = []

    if fresh_state_needed:
        db_connection = create_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT coins_list FROM coins WHERE exchange = %s', ['cryptopia'])
        coins_list = db_cursor.fetchone()[0]
        db_connection.close()
    else:
        if not _cryptopia_coins_list:
            coins_list = fetch_all_cryptopia_coins(True)
        else:
            coins_list = _cryptopia_coins_list

    return coins_list


def fetch_all_group_ids(fresh_state_needed):
    groups_list = []

    if fresh_state_needed:
        db_connection = create_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT group_id, signal_type FROM pump_groups')
        groups_list = db_cursor.fetchall()
        db_connection.close()
    else:
        if not _all_groups_list:
            groups_list = fetch_all_group_ids(True)
        else:
            groups_list = _all_groups_list

    return groups_list


def fetch_text_signal_groups(fresh_state_needed):
    return _text_groups_list if not fresh_state_needed and _text_groups_list else \
        [group[0] for group in fetch_all_group_ids(fresh_state_needed) if group[1] == 'text']


def fetch_image_signal_groups(fresh_state_needed):
    return _image_groups_list if not fresh_state_needed and _image_groups_list else \
        [group[0] for group in fetch_all_group_ids(fresh_state_needed) if group[1] == 'image']


def fetch_unknown_signal_groups(fresh_state_needed):
    return _unknown_groups_list if not fresh_state_needed and _unknown_groups_list else \
        [group[0] for group in fetch_all_group_ids(fresh_state_needed) if group[1] == 'unknown']


_all_groups_list = fetch_all_group_ids(True)
_text_groups_list = fetch_text_signal_groups(True)
_image_groups_list = fetch_image_signal_groups(True)
_unknown_groups_list = fetch_unknown_signal_groups(True)

_yobit_coins_list = fetch_all_yobit_coins(True)
_cryptopia_coins_list = fetch_all_cryptopia_coins(True)
