from common.database.database_connection import obtain_db_connection


def fetch_all_groups(fresh_state_needed):
    groups_list = []

    if fresh_state_needed:
        db_connection = obtain_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT group_id, signal_type FROM pump_groups')
        groups_list = db_cursor.fetchall()
        db_connection.close()
    else:
        if not all_groups_list:
            groups_list = fetch_all_groups(True)
        else:
            groups_list = all_groups_list

    return groups_list


def fetch_text_signal_groups(fresh_state_needed):
    return text_groups_list if not fresh_state_needed and text_groups_list else \
        [group[0] for group in fetch_all_groups(fresh_state_needed) if group[1] == 'text']


def fetch_image_signal_groups(fresh_state_needed):
    return image_groups_list if not fresh_state_needed and image_groups_list else \
        [group[0] for group in fetch_all_groups(fresh_state_needed) if group[1] == 'image']


def fetch_unknown_signal_groups(fresh_state_needed):
    return unknown_groups_list if not fresh_state_needed and unknown_groups_list else \
        [group[0] for group in fetch_all_groups(fresh_state_needed) if group[1] == 'unknown']


all_groups_list = fetch_all_groups(True)
text_groups_list = fetch_text_signal_groups(True)
image_groups_list = fetch_image_signal_groups(True)
unknown_groups_list = fetch_unknown_signal_groups(True)
