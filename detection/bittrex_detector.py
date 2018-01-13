import time

from detection.bittrex_constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD, ITERATIONS_COUNT, SNAPSHOT_FREQUENCY_SEC
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

            print('we have ', coins_snapshot_count, ' snapshots ready')

            # calculate the differences only if all required snapshots have been made
            if coins_snapshot_count >= ITERATIONS_COUNT:
                print('now calculating..')
                last_coins_snapshot = self.coins_snapshots_list[-1]

                for index in range(0, ITERATIONS_COUNT - 1):
                    # extract two snapshots adjacent in time and compare them to each other
                    previous_coins_snapshot = self.coins_snapshots_list[index]
                    current_coins_snapshot = self.coins_snapshots_list[index + 1]

                    for current_snapshot_coin in current_coins_snapshot:
                        if current_snapshot_coin['BaseVolume'] >= MIN_BTC_VOLUME:
                            previous_snapshot_coin = next((item for item in previous_coins_snapshot if item['MarketName'] == current_snapshot_coin['MarketName']))
                            print("")
                            print('Previous snapshot coin', previous_snapshot_coin)
                            print('Current snapshot coin', current_snapshot_coin)
                            print("")
                            if previous_snapshot_coin is not None and current_snapshot_coin['Ask'] > previous_snapshot_coin['Ask'] * MIN_SOAR_THRESHOLD:
                                print('Bittrex pump: ', previous_snapshot_coin['MarketName'], ', was: ', previous_snapshot_coin['Ask'], ', is: ',
                                      current_snapshot_coin['Ask'])

                                unwanted_keys = set(current_snapshot_coin.keys()) - WANTED_KEYS
                                for unwanted_key in unwanted_keys:
                                    del current_snapshot_coin[unwanted_key]

                del self.coins_snapshots_list[0]
                # delete the oldest coins snapshot

            time.sleep(SNAPSHOT_FREQUENCY_SEC)
