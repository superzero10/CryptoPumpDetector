from telegram_pumps.database.database_retriever import *
from telegram_pumps.database.database_writer import DatabaseWriter
from telegram_pumps.pump_coin_extraction.signal_message_recognition import PumpCoinExtractor


class MessagesHandler:
    _all_groups_id_list = []
    _text_signal_groups = []
    _image_signal_groups = []
    _unknown_signal_groups = []

    _coin_extractor = PumpCoinExtractor()
    _database_writer = DatabaseWriter()

    def __init__(self):
        self.__refresh_fetched_groups()

    def __refresh_fetched_groups(self):
        self._all_groups_id_list = [group[0] for group in fetch_all_group_ids(True)]
        self._text_signal_groups = fetch_text_signal_groups(True)
        self._image_signal_groups = fetch_image_signal_groups(True)
        self._unknown_signal_groups = fetch_unknown_signal_groups(True)

    def handle_data_updates(self, message):
        group_id = message.to_id.channel_id
        message_text = message.message

        if 'joinchat' in message_text:
            return None

        self.__process_text_signal_group_message(message_text)

        # if group_id in self._text_signal_groups:
        # self.__process_text_signal_group_message(message_text)

        if group_id in self._image_signal_groups:
            self.__process_image_signal_group_message(message)

        if group_id in self._unknown_signal_groups:
            self._database_writer.save_unknown_group_message(message)

        if group_id not in self._all_groups_id_list:
            print('- Message from a non-listed group, saving message and group to db..')
            self._database_writer.save_unlisted_group(group_id)
            self.__refresh_fetched_groups()
            self._database_writer.save_unknown_group_message(message)

    def __process_text_signal_group_message(self, message_text):
        self._coin_extractor.extract_pump_signal(message_text)

        minutes_to_pump = self._coin_extractor.extract_minutes_to_pump(message_text)
        if minutes_to_pump:
            print(
                '/////////////////////////////////////////////////////////////////////////////////\nFOUND PUMP ANNOUNCEMENT: ',
                minutes_to_pump,
                ' MINUTES TO PUMP\n/////////////////////////////////////////////////////////////////////////////////')

    def __process_image_signal_group_message(self, message):
        print('- Message from an image signal group \n')
