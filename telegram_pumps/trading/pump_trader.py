import time
from datetime import datetime

from telegram_pumps.pump_coin_extraction.recent_trades_memory import RecentTradeMemoryQueue


class PumpTrader:
    _PUMP_COIN_HOLD_SECONDS = 15
    recent_trades_queue = RecentTradeMemoryQueue()

    def trade_pumped_coin(self, coin, exchange):
        print(datetime.time(datetime.now()), '|||||||||| PUMP DETECTED, coin:', coin, 'exchange:', exchange)
        self.__buy_coin(coin, exchange)
        # hold the coin for
        time.sleep(15)
        self.__sell_coin(coin, exchange)

    def __buy_coin(self, coin, exchange):
        pass

    def __sell_coin(self, coin, exchange):
        pass
