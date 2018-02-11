import re


class PumpCoinRecognizer:

    def is_probable_pump_signal(self, message_text):
        pass

    def is_probable_pump_time_announcement(self, message_text):

        if message_text.strip().isdigit():
            return True

        prepared_text = message_text.replace(" ", "").lower()

