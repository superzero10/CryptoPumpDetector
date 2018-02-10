from telegram_pumps.database.database_retriever import *
from telegram_pumps.unknown_tracing.unknown_group_message_tracer import save_unknown_group_message

all_groups_id_list = fetch_all_groups(True)
text_signal_groups = fetch_text_signal_groups(True)
image_signal_groups = fetch_image_signal_groups(True)
unknown_signal_groups = fetch_unknown_signal_groups(True)


def handle_data_updates(message):
    print(message)
    message_channel_id = message.to_id.channel_id

    if message_channel_id not in all_groups_id_list or message_channel_id in unknown_signal_groups:
        save_unknown_group_message(message)
        print('Message from non-listed group or from a group whose signal type is unknown, saving message to db..')

    if message_channel_id in text_signal_groups:
        _process_text_signal_group_message(message)

    if message_channel_id in image_signal_groups:
        _process_image_signal_group_message(message)


def _process_text_signal_group_message(message):
    print('Processing a message from a text signal group')


def _process_image_signal_group_message(message):
    print('Processing a message from an image signal group')
