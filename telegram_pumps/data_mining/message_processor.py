from datetime import datetime
from itertools import count
from time import time

from telegram_pumps.data_mining.expected_pumps_handler import ExpectedPumpsHandler
from telegram_pumps.database.database_retriever import *
from telegram_pumps.database.database_writer import DatabaseWriter
from telegram_pumps.pump_coin_extraction.signal_message_recognition import MessageInfoExtractor
from telegram_pumps.trading.pump_trader import PumpTrader


class MessageProcessor:
    _ids = count(0)

    _all_groups_id_list = []
    _text_signal_groups = []
    _image_signal_groups = []
    _unknown_signal_groups = []

    _waste_message_fragments = ['joinchat', 't.me/', 'register', 'sign', 'timeanddate', 'youtu.be', 'promo']
    _cross_promo_link_parts = ['joinchat', 't.me/']

    _info_extractor = MessageInfoExtractor()
    _database_writer = DatabaseWriter()
    _expected_pumps_handler = ExpectedPumpsHandler()
    _pump_trader = PumpTrader()

    def __init__(self):
        self.id = next(self._ids)
        self.__refresh_fetched_groups()
        print(self.id)

    def __refresh_fetched_groups(self):
        self._all_groups_id_list = [group[0] for group in fetch_all_group_ids(True)]
        self._text_signal_groups = fetch_text_signal_groups(True)
        self._image_signal_groups = fetch_image_signal_groups(True)
        self._unknown_signal_groups = fetch_unknown_signal_groups(True)

    def handle_messages(self, message):
        message_receive_timestamp = time()
        group_id = message.to_id.channel_id
        message_text = message.message

        if any(unwanted in message_text for unwanted in self._waste_message_fragments) or not message_text:
            if any(promo_link_part in message_text for promo_link_part in self._cross_promo_link_parts):
                self.save_unique_cross_promo_group_links(message_text)
            return None

        self.__process_text_signal_group_message(message_text, group_id)
        self.__collect_message_statistics(message, message_receive_timestamp, group_id)

        # if group_id in self._text_signal_groups:
        # self.__process_text_signal_group_message(message_text)

        # if group_id in self._image_signal_groups:
        #     self.__process_image_signal_group_message(message)

        # if group_id in self._unknown_signal_groups:
        # self._database_writer.save_unknown_group_message(message)

        if group_id not in self._all_groups_id_list:
            print(datetime.time(datetime.now()), '- Message from a non-listed group, saving message and group to db..')
            self._database_writer.save_unlisted_group(group_id)
            self.__refresh_fetched_groups()
            self._database_writer.save_unknown_group_message(message)

    def save_unique_cross_promo_group_links(self, message_text):
        self._database_writer.save_cross_promo_links(self.__find_cross_promo_links(message_text))

    def __find_cross_promo_links(self, message_text):
        all_links = self._info_extractor.extract_message_links(message_text)
        return [link for link in all_links if any(part in link for part in self._cross_promo_link_parts)]

    def __process_text_signal_group_message(self, message_text, group_id):
        print(message_text)
        coin_from_link, exchange_from_link = self._info_extractor.extract_pump_signal_from_link(message_text)
        print(message_text)

        # if there's a pump signal with direct link to the exchange, trade it immediately without checking if pump was expected
        if coin_from_link and exchange_from_link:
            self.__trade_on_pump_signal(coin_from_link, exchange_from_link)
            return

        coin = self._info_extractor.extract_possible_pump_signal(message_text)
        minutes_to_pump, pump_exchange = self._info_extractor.extract_pump_minutes_and_exchange_if_present(message_text)
        self._expected_pumps_handler.save_expected_pump_time_if_present(group_id, minutes_to_pump)
        self._expected_pumps_handler.save_expected_pump_exchange_if_present(group_id, pump_exchange)

        if coin:  # if no exchange found, it can be extracted from expected exchanges list
            # found a coin in the message, now need to check if a pump in this channel was expected at this exact time
            if not pump_exchange:
                pump_exchange = self._expected_pumps_handler.get_expected_exchange(group_id)
            if not pump_exchange:
                pump_exchange = self._info_extractor.get_exchange_if_exclusive_coin(coin)
            self.__process_pump_if_was_expected(coin, pump_exchange, group_id)

    def __collect_message_statistics(self, message, receive_timestamp, group_id):
        message_receive_timestamp = int(receive_timestamp)
        message_send_timestamp = int(message.date.timestamp())

        if (message_receive_timestamp - message_send_timestamp) in range(3599, 3600 * 24):
            message_send_timestamp += 3600  # add 1 hour in case of Moscow timezone

        self._database_writer.save_processed_message(
            message=message.message.replace('\n', ''),
            group_id=group_id,
            timestamp=message_send_timestamp,
            receive_time=str(datetime.utcfromtimestamp(message_receive_timestamp)),
            send_time=str(datetime.utcfromtimestamp(message_send_timestamp)),
            processing_time=time() - receive_timestamp,
            delay_sec=message_receive_timestamp - message_send_timestamp
        )

    def __trade_on_pump_signal(self, coin, exchange):
        self._pump_trader.trade_pumped_coin_if_viable(coin, exchange)

    def __process_pump_if_was_expected(self, coin, exchange, group_id):
        if self._expected_pumps_handler.is_within_expected_pump_date_range(group_id):
            self.__trade_on_pump_signal(coin, exchange)
        else:
            print(datetime.time(datetime.now()), '++ Nope, didn\'t expect a pump here')

    def __process_image_signal_group_message(self, message):
        print(datetime.time(datetime.now()), '- Message from an image signal group')
