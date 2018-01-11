import time

from detection.bittrex_constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD, ITERATIONS_COUNT, \
    SERVER_REQUEST_FREQUENCY_SEC
from exchange_services.bittrex_service import BittrexService

WANTED_KEYS = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}
BTC_PAIR_PREFIX = 'BTC-'


class BittrexDetector:

    apiService = BittrexService()
    new_coin_data = apiService.fetch_btc_coin_data()
    coins_snapshots_list = []

    def detect(self):
        while True:
            active_btc_pairs = self.apiService.fetch_active_btc_pairs()

            self.coins_snapshots_list.append(self.apiService.fetch_btc_coin_data())
            coins_snapshot_count = len(self.coins_snapshots_list)

            if coins_snapshot_count >= ITERATIONS_COUNT:

                # take all snapshots but last to which the rest will be compared
                for coins_snapshot in self.coins_snapshots_list[:coins_snapshot_count - 1]:
                    for coin_data in coins_snapshot:
                        # check if coin has higher price than all of the previous queue items
                        if str(coin_data['MarketName']).startswith(BTC_PAIR_PREFIX) and coin_data['BaseVolume'] >= MIN_BTC_VOLUME:
                            old_coin = next((item for item in coin_data['result'] if item['MarketName'] == coin_data['MarketName']))
                            if old_coin is not None and coin_data['Ask'] > old_coin['Ask'] * MIN_SOAR_THRESHOLD:
                                print('Bittrex pump: ', old_coin['MarketName'], ', was: ', old_coin['Ask'], ', is: ', coin_data['Ask'])

                                unwanted_keys = set(coin_data.keys()) - WANTED_KEYS
                                for unwanted_key in unwanted_keys:
                                    del coin_data[unwanted_key]

                del self.coins_snapshots_list[0]
                # delete the oldest coins snapshot

            time.sleep(SERVER_REQUEST_FREQUENCY_SEC)
