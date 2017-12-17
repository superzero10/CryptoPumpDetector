import requests
import math

BTC_POSTFIX = '_btc'
ADMISSABLE_PAIRS_COUNT = 57


class YobitService:
    @staticmethod
    def fetch_active_btc_pairs():
        active_pairs_response = requests.get("https://yobit.net/api/3/info").json()
        active_pairs = active_pairs_response['pairs']
        btc_pairs_dict_keys = {key: value for key, value in active_pairs.items() if
                               str(key).endswith(BTC_POSTFIX)}.keys()
        return list(btc_pairs_dict_keys)

    @staticmethod
    def fetch_btc_coins_data():
        result = {}
        btc_pairs = YobitService.fetch_active_btc_pairs()
        for index in range(int(math.ceil(len(btc_pairs) / ADMISSABLE_PAIRS_COUNT))):
            start_index = index * ADMISSABLE_PAIRS_COUNT
            end_index = start_index + ADMISSABLE_PAIRS_COUNT - 1
            divided_query_pairs = '-'.join(btc_pairs[start_index:end_index])

            market_request = 'https://yobit.net/api/3/ticker/' + divided_query_pairs + '?ignore_invalid=1'
            market_response = requests.get(market_request).json()
            # print(market_response)
            result.update(market_response)
        return result
