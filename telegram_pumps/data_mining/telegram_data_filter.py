from telegram_pumps.database.database_retriever import *
from telegram_pumps.database.database_writer import save_unknown_group_message, save_unlisted_group

all_groups_id_list = [group[0] for group in fetch_all_group_ids(True)]
text_signal_groups = fetch_text_signal_groups(True)
image_signal_groups = fetch_image_signal_groups(True)
unknown_signal_groups = fetch_unknown_signal_groups(True)


def handle_data_updates(message):
    group_id = message.to_id.channel_id

    if group_id not in all_groups_id_list:
        print('- Message from non-listed group, saving message to db..')
        save_unlisted_group(group_id)
        save_unknown_group_message(message)

    if group_id in unknown_signal_groups:
        print('- Message from a group whose signal type is unknown, saving message to db..')
        save_unknown_group_message(message)

    if group_id in text_signal_groups:
        _process_text_signal_group_message(message)

    if group_id in image_signal_groups:
        _process_image_signal_group_message(message)


def _process_text_signal_group_message(message):
    print('- Message from a text signal group')


def _process_image_signal_group_message(message):
    print('- Message from an image signal group')
