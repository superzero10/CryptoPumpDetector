from telegram_pumps.database.database_retriever import *
from telegram_pumps.database.database_writer import save_unknown_group_message, save_unlisted_group


class MessagesHandler:
    _all_groups_id_list = []
    _text_signal_groups = []
    _image_signal_groups = []
    _unknown_signal_groups = []

    def __init__(self):
        self.__refresh_fetched_groups()

    def __refresh_fetched_groups(self):
        self._all_groups_id_list = [group[0] for group in fetch_all_group_ids(True)]
        self._text_signal_groups = fetch_text_signal_groups(True)
        self._image_signal_groups = fetch_image_signal_groups(True)
        self._unknown_signal_groups = fetch_unknown_signal_groups(True)

    def __process_text_signal_group_message(self, message):
        print('- Message from a text signal group \n')

    def __process_image_signal_group_message(self, message):
        print('- Message from an image signal group \n')

    def handle_data_updates(self, message):
        group_id = message.to_id.channel_id

        if group_id in self._text_signal_groups:
            self.__process_text_signal_group_message(message)

        if group_id in self._image_signal_groups:
            self.__process_image_signal_group_message(message)

        if group_id in self._unknown_signal_groups:
            print('- Message from a group whose signal type is unknown, saving message to db..')
            save_unknown_group_message(message)

        if group_id not in self._all_groups_id_list:
            print('- Message from a non-listed group, saving message and group to db..')
            save_unlisted_group(group_id)
            self.__refresh_fetched_groups()
            save_unknown_group_message(message)
