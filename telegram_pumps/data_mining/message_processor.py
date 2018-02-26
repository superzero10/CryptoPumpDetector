from time import time

from telegram_pumps.database.database_retriever import *
from telegram_pumps.database.database_writer import DatabaseWriter
from telegram_pumps.pump_coin_extraction.signal_message_recognition import MessageInfoExtractor


class MessageProcessor:
    _all_groups_id_list = []
    _text_signal_groups = []
    _image_signal_groups = []
    _unknown_signal_groups = []

    _waste_message_fragments = ['joinchat', 't.me/', 'register', 'sign']
    _exchange_names = ['yobit', 'coinexchange', 'cryptopia', 'binance']
    _exchange_coin_links_prefixes = ['https://yobit', 'https://www.coinexchange.io', 'https://www.cryptopia',
                                     'https://www.binance.com']

    _expected_pump_timestamps = {}  # (group_id, timestamp)
    _expected_pump_exchanges = {}  # (group_id, dict{ex1, ex2, ex3])

    _info_extractor = MessageInfoExtractor()
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

        if any(unwanted in message_text for unwanted in self._waste_message_fragments) or not message_text:
            return None

        self.__process_text_signal_group_message(message_text, group_id)

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

    def __process_text_signal_group_message(self, message_text, group_id):
        exchange, coin = self._info_extractor.extract_pump_signal(message_text)
        print('|||||||||| PUMP DETECTED at: ', exchange, 'coin: ', coin)

        self.__handle_expected_pump_time(group_id, message_text)
        self.__handle_expected_pump_exchange(group_id, message_text)

    def __handle_expected_pump_time(self, group_id, message_text):
        minutes_to_pump = self._info_extractor.extract_minutes_to_pump(message_text)
        if minutes_to_pump:
            print('FOUND PUMP ANNOUNCEMENT: ', minutes_to_pump, ' MINUTES TO PUMP\n')
            self._expected_pump_timestamps.pop(group_id, None)
            self._expected_pump_timestamps[group_id] = time() + minutes_to_pump * 60
            print('EXPECTED PUMPS SET: ', self._expected_pump_timestamps)

    def __handle_expected_pump_exchange(self, group_id, message_text):
        for exchange_name in self._exchange_names:
            if exchange_name in message_text.lower():
                print('FOUND PUMP EXCHANGE: ', exchange_name, '\n')
                self._expected_pump_exchanges.pop(group_id, None)
                self._expected_pump_exchanges[group_id] = exchange_name

    def __process_image_signal_group_message(self, message):
        print('- Message from an image signal group \n')
