import time
from datetime import datetime

from detection.bittrex_constants import MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD, SNAPSHOT_COUNT, SNAPSHOT_FREQUENCY_SEC

from common.exchange_services import BittrexService

WANTED_KEYS = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}
BTC_PAIR_PREFIX = 'BTC-'


class BittrexDetector:
    apiService = BittrexService()
    new_coin_data = apiService.fetch_btc_coin_data()
    coins_snapshots_list = []

    def detect(self):

        print(datetime.time(datetime.now()), 'Bittrex detection started')

        while True:
            active_btc_pairs = self.apiService.fetch_active_btc_pairs()
            possible_coin_names = []

            self.coins_snapshots_list.append(self.apiService.fetch_btc_coin_data())
            coins_snapshot_count = len(self.coins_snapshots_list)

            # calculate the differences only if all required snapshots have been captured
            if coins_snapshot_count >= SNAPSHOT_COUNT:

                first_coins_snapshot = self.coins_snapshots_list[0]
                last_coins_snapshot = self.coins_snapshots_list[-1]

                # possible_coin_names = [coin['MarketName'] for coin in last_coins_snapshot]
                possible_coins = []

                for coin in last_coins_snapshot:
                    if coin['BaseVolume'] >= MIN_BTC_VOLUME:
                        old_coin = next(
                            item for item in first_coins_snapshot if item['MarketName'] == coin['MarketName'])
                        if old_coin is not None and coin['Ask'] > old_coin['Ask'] * MIN_SOAR_THRESHOLD:
                            if old_coin['Ask'] == 0:
                                old_coin['Ask'] = 1  # to prevent zero division
                            possible_coins.append((coin['MarketName'], coin['Ask'], old_coin['Ask'],
                                                   coin['Ask'] / old_coin['Ask'] * 100))

                # for index in range(0, ITERATIONS_COUNT - 1):
                #     previous_coins_snapshot = self.coins_snapshots_list[index]
                #     current_coins_snapshot = self.coins_snapshots_list[index + 1]
                #
                #     for current_snapshot_coin in current_coins_snapshot:
                #         if current_snapshot_coin['BaseVolume'] >= MIN_BTC_VOLUME:
                #             previous_snapshot_coin = next((item for item in previous_coins_snapshot if item['MarketName'] == current_snapshot_coin['MarketName']))
                #             # print(datetime.time(datetime.now()), "")
                #             # print(datetime.time(datetime.now()), 'Previous snapshot coin', previous_snapshot_coin)
                #             # print(datetime.time(datetime.now()), 'Current snapshot coin', current_snapshot_coin)
                #
                #             if previous_snapshot_coin is not None and current_snapshot_coin['Ask'] > previous_snapshot_coin['Ask'] * MIN_SOAR_THRESHOLD:
                #                 print(datetime.time(datetime.now()), 'Bittrex pump: ', previous_snapshot_coin['MarketName'], ', was: ', previous_snapshot_coin['Ask'], ', is: ',
                #                       current_snapshot_coin['Ask'])
                #
                #                 unwanted_keys = set(current_snapshot_coin.keys()) - WANTED_KEYS
                #                 for unwanted_key in unwanted_keys:
                #                     del current_snapshot_coin[unwanted_key]

                if possible_coins:
                    for possible_coin in possible_coins:
                        print(datetime.time(datetime.now()), possible_coin)

                # delete the oldest coins snapshot
                del self.coins_snapshots_list[0]

            time.sleep(SNAPSHOT_FREQUENCY_SEC)
