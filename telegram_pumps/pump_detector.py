from telegram_pumps.data_mining.message_processor import MessageProcessor
from telegram_pumps.data_mining.telegram_api_client import TelegramApiClient


class PumpDetector:
    _message_processor = MessageProcessor()

    def __init__(self):
        TelegramApiClient(self._message_processor.handle_messages)


if __name__ == '__main__':
    PumpDetector()
