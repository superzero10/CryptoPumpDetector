from datetime import datetime

import math
import requests


class YobitService:
    _BTC_POSTFIX = '_btc'
    _PAIRS_PER_REQUEST = 57
    _RESULT = 'pairs'

    def fetch_active_btc_pairs(self):
        active_pairs_response = requests.get("https://yobit.net/api/3/info").json()
        active_pairs = active_pairs_response[self._RESULT]
        btc_pairs_dict_keys = {key: value for key, value in active_pairs.items() if
                               str(key).endswith(self._BTC_POSTFIX)}.keys()
        return [coin[:-4] for coin in list(btc_pairs_dict_keys)]  # ltc_btc -> ltc

    def fetch_btc_coins_data(self):
        result = {}
        btc_pairs = self.fetch_active_btc_pairs()
        for index in range(int(math.ceil(len(btc_pairs) / self._PAIRS_PER_REQUEST))):
            start_index = index * self._PAIRS_PER_REQUEST
            end_index = start_index + self._PAIRS_PER_REQUEST - 1
            divided_query_pairs = '-'.join(btc_pairs[start_index:end_index])

            market_request = 'https://yobit.net/api/3/ticker/' + divided_query_pairs + '?ignore_invalid=1'
            market_response = requests.get(market_request)
            try:
                market_response = market_response.json()
                result.update(market_response)
            except:
                print(datetime.time(datetime.now()), market_response.content)

        return result


print(YobitService().fetch_active_btc_pairs())
