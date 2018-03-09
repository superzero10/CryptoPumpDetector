from telegram_pumps.pump_coin_extraction.recent_trades_memory import RecentTradeMemoryQueue


class PumpTrader:
    recent_trades_queue = RecentTradeMemoryQueue()

    coinexchange_coins = []
    yobit_coins = []
    cryptopia_coins = []
    binance_coins = []
