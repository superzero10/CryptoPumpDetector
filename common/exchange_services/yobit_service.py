import math
import requests

BTC_POSTFIX = '_btc'
PAIRS_PER_REQUEST = 57
RESULT = 'pairs'


class YobitService:

    def fetch_active_btc_pairs(self):
        active_pairs_response = requests.get("https://yobit.net/api/3/info").json()
        active_pairs = active_pairs_response[RESULT]
        btc_pairs_dict_keys = {key: value for key, value in active_pairs.items() if
                               str(key).endswith(BTC_POSTFIX)}.keys()
        return list(btc_pairs_dict_keys)

    def fetch_btc_coins_data(self):
        result = {}
        btc_pairs = self.fetch_active_btc_pairs()
        for index in range(int(math.ceil(len(btc_pairs) / PAIRS_PER_REQUEST))):
            start_index = index * PAIRS_PER_REQUEST
            end_index = start_index + PAIRS_PER_REQUEST - 1
            divided_query_pairs = '-'.join(btc_pairs[start_index:end_index])

            market_request = 'https://yobit.net/api/3/ticker/' + divided_query_pairs + '?ignore_invalid=1'
            market_response = requests.get(market_request)
            try:
                market_response = market_response.json()
                result.update(market_response)
            except:
                print(market_response.content)

        return result
