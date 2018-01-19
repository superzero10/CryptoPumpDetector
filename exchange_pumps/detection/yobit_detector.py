import queue

from detection.yobit_constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD
from common.exchange_services import YobitService


class YobitDetector:

    apiService = YobitService()
    active_btc_pairs = apiService.fetch_active_btc_pairs()
    new_coin_data = apiService.fetch_btc_coins_data()

    def detect(self):
        # print('Yobit thread started at ', time.time()

        coin_data = self.new_coin_data
        self.new_coin_data = self.apiService.fetch_btc_coins_data()
        for coin_name, coin in self.new_coin_data.items():
            if coin_name in coin_data and coin['vol'] >= MIN_BTC_VOLUME:
                old_coin = coin_data[coin_name]
                if old_coin is not None and coin['sell'] >= old_coin['sell'] * MIN_SOAR_THRESHOLD:
                    print('Yobit coin soaring: ', coin_name, ', was: ', old_coin['sell'], ', is: ', coin['sell'])

        q = queue.Queue(10)

