from telegram_pumps.message_processor import MessageProcessor
from telegram_pumps.pump_trader import PumpTrader
from telegram_pumps.telegram_api_client import TelegramApiClient


class PumpDetector:
    _message_processor = MessageProcessor()
    _pump_trader = PumpTrader()

    def __init__(self):
        TelegramApiClient(self._message_processor.handle_messages)


if __name__ == '__main__':
    PumpDetector()
