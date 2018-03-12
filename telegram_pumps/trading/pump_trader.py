import time
from datetime import datetime

from common.exchange_services.cryptopia_service import CryptopiaService
from common.exchange_services.yobit_service import YobitService


class PumpTrader:

    _PUMP_COIN_HOLD_SECONDS = 15

    _yobit_service = YobitService()
    _cryptopia_service = CryptopiaService()

    def trade_pumped_coin(self, coin, exchange):
        print(datetime.time(datetime.now()), '|||||||||| PUMP DETECTED, coin:', coin, 'exchange:', exchange)
        self.__buy_coin(coin, exchange)
        time.sleep(self._PUMP_COIN_HOLD_SECONDS)
        self.__sell_coin(coin, exchange)

    def __buy_coin(self, coin, exchange):
        time.sleep(3)
        print('BOUGHT COIN', coin, 'ON EXCHANGE', exchange)
        pass

    def __sell_coin(self, coin, exchange):
        time.sleep(3)
        print('SOLD COIN', coin, 'ON EXCHANGE', exchange)
