import requests

RESULT = "result"
MARKET_NAME = "MarketName"
MARKET_SHORT_NAME = "MarketCurrency"
MARKET_LONG_NAME = "MarketCurrencyLong"
IS_ACIVE = "IsActive"
BTC_PREFIX = "BTC"


class BittrexService:
    market_summaries_request = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
    all_markets_request = "https://bittrex.com/api/v1.1/public/getmarkets"

    def fetch_btc_coin_data(self):
        return requests.get(self.market_summaries_request).json()

    def fetch_active_btc_pairs(self):
        coin_list = []
        coin_data = self.fetch_btc_coin_data()
        for coin in coin_data[RESULT]:
            if str(coin[MARKET_NAME]).startswith(BTC_PREFIX):
                coin_list.append(coin[MARKET_NAME])

        return coin_list

    def fetch_active_btc_pairs_with_names(self):
        result = []
        markets_data = requests.get(self.all_markets_request).json()
        for market in markets_data[RESULT]:
            if str(market[MARKET_NAME]).startswith(BTC_PREFIX) and market[IS_ACIVE]:
                market_name_variants_list = [market[MARKET_SHORT_NAME], market[MARKET_LONG_NAME]]

                if market[MARKET_LONG_NAME] != market[MARKET_LONG_NAME].capitalize():
                    market_name_variants_list.append(market[MARKET_LONG_NAME].capitalize())

                if market[MARKET_LONG_NAME].lower().endswith("coin"):
                    market_name_variants_list.append(market[MARKET_LONG_NAME][:-4])

                result.append(market_name_variants_list)

        return result


print(BittrexService().fetch_active_btc_pairs_with_names())
