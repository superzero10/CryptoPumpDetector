import threading
import time
from datetime import datetime
from threading import Lock
from time import time

from common.exchange_services.cryptopia_service import CryptopiaService
from common.exchange_services.yobit_service import YobitService


class PumpTrader:

    _PUMP_COIN_HOLD_SECONDS = 15

    _yobit_service = YobitService()
    _cryptopia_service = CryptopiaService()
    _lock = Lock()

    _recently_traded_coins = []  # [(coin, exchange, timestamp)]

    def trade_pumped_coin_if_viable(self, coin, exchange):
        print(datetime.time(datetime.now()), '||| PUMP DETECTED, coin:', coin, 'exchange:', exchange)

        with self._lock:
            if (coin, exchange) not in [(t_coin, t_exchange) for (t_coin, t_exchange, t_timestamp) in
                                        self._recently_traded_coins]:
                # if coin was not traded ever
                # create a new thread for each trade process
                trade_thread = threading.Thread(target=self.__trade_coin(coin, exchange))
                trade_thread.start()
            else:
                print('|||||| COIN ', coin, 'WAS TRADED RECENTLY ON', exchange, 'ABORTING...')

    def __trade_coin(self, coin, exchange):
        self.__buy_coin(coin, exchange)
        time.sleep(self._PUMP_COIN_HOLD_SECONDS)
        self.__sell_coin(coin, exchange)

    def __buy_coin(self, coin, exchange):
        print(datetime.time(datetime.now()), '||||||||| BOUGHT COIN', coin, 'ON EXCHANGE', exchange)
        self._recently_traded_coins.append((coin, exchange, time.time()))

    def __sell_coin(self, coin, exchange):
        print(datetime.time(datetime.now()), '||||||||| SOLD COIN', coin, 'ON EXCHANGE', exchange)
