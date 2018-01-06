import datetime
import time

from database.database_connection import obtain_db_connection
from detection.constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD
from exchange_services.bittrex_service import BittrexService

WANTED_KEYS = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}
BTC_PAIR_PREFIX = 'BTC-'


class BittrexDetector:

    apiService = BittrexService()
    new_coin_data = apiService.fetch_btc_coin_data()
    db_connection = None

    def detect(self):
        active_btc_pairs = self.apiService.fetch_active_btc_pairs()

        current_timestamp = time.time()
        current_time = datetime.datetime.now().time()

        coin_data = self.new_coin_data
        self.new_coin_data = self.apiService.fetch_btc_coin_data()
        for coin in self.new_coin_data['result']:
            if str(coin['MarketName']).startswith(BTC_PAIR_PREFIX) and coin['BaseVolume'] >= MIN_BTC_VOLUME:
                old_coin = next((item for item in coin_data['result'] if item['MarketName'] == coin['MarketName']))
                if old_coin is not None and coin['Ask'] >= old_coin['Ask'] * MIN_SOAR_THRESHOLD:
                    print('Bittrex pump: ', old_coin['MarketName'], ', was: ', old_coin['Ask'], ', is: ', coin['Ask'])

                    unwanted_keys = set(coin.keys()) - WANTED_KEYS
                    for unwanted_key in unwanted_keys:
                        del coin[unwanted_key]
