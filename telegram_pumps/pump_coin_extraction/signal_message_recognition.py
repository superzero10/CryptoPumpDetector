import re
from datetime import datetime

from common.exchange_services.cryptopia_service import CryptopiaService
from common.exchange_services.yobit_service import YobitService


class MessageInfoExtractor:
    _letters_pattern = r'([^\s\w]|_)+'
    _alphanumerics_pattern = r'[\W_]+'
    _emoji_removing_pattern = r'\\[a-z0-9]{5}'
    _pump_minutes_pattern = r'\d+[" "]*min|\d+[" "]*минут'
    _coin_extraction_pattern = r'(?<=\b\w)[ ]{1,}(?![ ]{0,}\w{2})'
    _coin_link_pattern = r'[A-Z0-9]{2,}'
    _general_url_pattern = "(?P<url>https?://[^\s]+)"

    _serviced_exchange_names_url_parts = ['yobit.', 'cryptopia.']
    _serviced_exchange_names = ['yobit', 'coinexchange', 'cryptopia', 'binance']
    _ignored_coins = ['all', 'in', 'are', 'profit', 'coin', 'red', 'today', 'time', 'off', 'buy', 'go', 'start', 'hodl',
                      'post', 'net', 'send', 'can', 'best', 'hope', 'soon', 'btc', 'fly', 'net', 'money', 'max', 'team']

    _cryptopia_coins = [coin.center(len(coin) + 2) for coin in CryptopiaService().fetch_active_btc_pairs()]
    _cryptopia_coins_search_list = [coin.strip().upper()[::-1] for coin in _cryptopia_coins]

    _yobit_coins = [coin.center(len(coin) + 2) for coin in YobitService().fetch_active_btc_pairs()]
    _yobit_search_reverse_list = [coin.strip().upper()[::-1] for coin in _yobit_coins]

    def extract_possible_pump_signal(self, message_text):
        found_links, message_without_links = self.__extract_message_links(message_text)

        if found_links:
            pumped_coin, exchange = self.__search_for_coin_in_link(found_links)

            if pumped_coin and exchange:  # if found coin & exchange from link, return to the trading module
                return pumped_coin, exchange

        cleaned_message = self.__clear_message(message_without_links)
        print(datetime.time(datetime.now()), 'MESSAGE AFTER PROCESSING: "', cleaned_message, '"')

        found_cryptopia_coins = [coin for coin in self._cryptopia_coins if coin in cleaned_message]
        found_yobit_coins = [coin for coin in self._yobit_coins if coin in cleaned_message]

        if found_cryptopia_coins:
            print(datetime.time(datetime.now()), "------ FOUND CRYPTOPIA PUMP COINS: ", found_cryptopia_coins)
        if found_yobit_coins:
            print(datetime.time(datetime.now()), "------ FOUND YOBIT PUMP COINS: ", found_yobit_coins)

        all_coins = list(map(lambda x: x.strip(), found_yobit_coins + found_cryptopia_coins))
        found_coins = list(set([coin for coin in all_coins if coin not in self._ignored_coins]))

        # if multiple coins are present, it is possible that's no pump coin announcement

        print("-------- OVERALL FOUND COINS", found_coins)
        return (found_coins and found_coins[0]) or None, None

    def __extract_message_links(self, message_text):
        found_links = re.findall(self._general_url_pattern, message_text)
        return found_links, re.sub(self._general_url_pattern, '', message_text)

    def __search_for_coin_in_link(self, found_links):
        for link in found_links:
            # extracts coin if link points to the exchange
            # "https://yobit.net/en/trade/LKC/BTC"
            # "https://www.cryptopia.co.nz/Exchange/?market=XBY_BTC"

            processed_link = re.sub(self._alphanumerics_pattern, '', link.split('#')[0].replace('BTC', '')[::-1])
            reversed_coin_from_link = re.findall(self._coin_link_pattern, processed_link)[0]

            for exchange_name in self._serviced_exchange_names_url_parts:
                if exchange_name in link:
                    print(datetime.time(datetime.now()), "++++++ FOUND EXCHANGE LINK", link)
                    detected_coins = [reverse_coin[::-1] for reverse_coin in self.__search_reverse_list(exchange_name)
                                      if reverse_coin == reversed_coin_from_link]
                    pumped_coin = detected_coins and detected_coins[0] or None

                    return pumped_coin, exchange_name
        return None, None

    def __search_reverse_list(self, exchange_name):
        return self._yobit_search_reverse_list if exchange_name == 'yobit.' else self._cryptopia_coins_search_list

    def __clear_message(self, message):
        message_without_emoji = re.sub(self._emoji_removing_pattern, ' ', message).replace('\'', '').strip()
        message_without_special_chars = re.sub(self._letters_pattern, ' ', message_without_emoji)
        message_without_newlines = message_without_special_chars.replace('\n', ' ').replace('\r', '').replace('\t', '')
        return self.__apply_coin_extraction_pattern(message_without_newlines)

    def __apply_coin_extraction_pattern(self, message):
        normalized_message = re.sub(self._coin_extraction_pattern, '', message)
        return normalized_message.center(len(normalized_message) + 2).lower()

    def extract_pump_minutes_and_exchange_if_present(self, message_text):
        cleaned_message_text = self.__clear_message(message_text)

        if cleaned_message_text.isdigit() and 0 < int(cleaned_message_text) < 200:
            return cleaned_message_text, None  # some groups count down with messages which contain only minutes to pump
        else:
            return self.__find_minutes_to_pump(cleaned_message_text), self.__find_pump_exchange(cleaned_message_text)

    def __find_minutes_to_pump(self, cleaned_message):
        found_substrings = re.findall(self._pump_minutes_pattern, cleaned_message)
        if not found_substrings:
            return None
        return int(''.join((filter(str.isdigit, found_substrings[0]))))

    def __find_pump_exchange(self, cleaned_message):
        found_exchanges = [name for name in self._serviced_exchange_names if name in cleaned_message]
        if found_exchanges and found_exchanges[0]:
            return found_exchanges[0]
        else:
            return None


print(
    MessageInfoExtractor().extract_possible_pump_signal("FOUND EXCHANGE LINK https://yobit.io/en/trade/2BACCO/BTC#12H"))
