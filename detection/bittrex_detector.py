import datetime
import time

from database.database_connection import obtain_db_connection
from detection.constants import SERVER_REQUEST_FREQUENCY_SEC, MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD
from exchange_services.bittrex_service import BittrexService

WANTED_KEYS = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}


class BittrexDetector:

    new_coin_data = {}
    db_connection = None

    def __init__(self):
        print("start")
        active_btc_pairs = BittrexService.fetch_active_btc_pairs()
        new_coin_data = BittrexService.fetch_btc_coin_data()
        db_connection = obtain_db_connection()
        print(active_btc_pairs)

    def detect(self):
        print('Bittrex thread started at ', time.time())

        current_timestamp = time.time()
        current_time = datetime.datetime.now().time()

        coin_data = self.new_coin_data
        self.new_coin_data = BittrexService.fetch_btc_coin_data()
        for coin in self.new_coin_data['result']:
            if coin['BaseVolume'] >= MIN_BTC_VOLUME:
                old_coin = next((item for item in coin_data['result'] if item['MarketName'] == coin['MarketName']))
                if coin['Ask'] >= old_coin['Ask'] * MIN_SOAR_THRESHOLD:
                    print('Possible pump coin: ', old_coin['MarketName'], ', was: ', old_coin['Ask'], ', is: ',
                          coin['Ask'])

                    unwanted_keys = set(coin.keys()) - WANTED_KEYS
                    for unwanted_key in unwanted_keys:
                        del coin[unwanted_key]

        print(current_time)

        # db_cursor = connection.cursor()
        # db_cursor.execute('SELECT * FROM COMPANY;')
        # rows = db_cursor.fetchall()
        # for row in rows:
        #     print(row[0], row[1], )2


