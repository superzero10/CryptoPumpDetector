import requests

RESULT = "result"
MARKET_NAME = "MarketName"
BTC_PREFIX = "BTC"


class BittrexService:

    @staticmethod
    def fetch_btc_coin_data():
        bittrex_market_response = requests.get(
            "https://bittrex.com/api/v1.1/public/getmarketsummaries")
        return bittrex_market_response.json()

    @staticmethod
    def fetch_active_btc_pairs():
        coin_list = []
        coin_data = BittrexService.fetch_btc_coin_data()
        for coin in coin_data[RESULT]:
            if str(coin[MARKET_NAME]).startswith(BTC_PREFIX):
                coin_list.append(coin[MARKET_NAME])

        return coin_list
