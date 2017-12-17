import datetime
import time

from database.database_connection import obtain_db_connection
from detection.constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD
from exchange_services.yobit_service import YobitService


class YobitDetector:
    apiService = YobitService()
    active_btc_pairs = apiService.fetch_active_btc_pairs()
    new_coin_data = apiService.fetch_btc_coins_data()
    db_connection = obtain_db_connection()

    def detect(self):
        # print('Yobit thread started at ', time.time())

        current_timestamp = time.time()
        current_time = datetime.datetime.now().time()

        coin_data = self.new_coin_data
        self.new_coin_data = self.apiService.fetch_btc_coins_data()
        for coin_name, coin in self.new_coin_data.items():
            if coin['vol'] >= MIN_BTC_VOLUME:
                old_coin = coin_data[coin_name]
                if old_coin is not None and coin['sell'] >= old_coin['sell'] * MIN_SOAR_THRESHOLD:
                    print('Yobit coin soaring: ', coin_name, ', was: ', old_coin['sell'], ', is: ', coin['sell'])

        # db_cursor = connection.cursor()
        # db_cursor.execute('SELECT * FROM COMPANY;')
        # rows = db_cursor.fetchall()
        # for row in rows:
        #     print(row[0], row[1], )2
