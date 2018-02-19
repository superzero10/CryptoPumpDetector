import re


class PumpCoinExtractor:

    def is_probable_pump_signal(self, message_text):
        pass

    def is_probable_pump_time_announcement(self, message):
        message_text = message.lower()
        regex = r'\d+[" "]*["min"|"минут"]+'
        print(re.findall(regex, message_text))


PumpCoinExtractor().is_probable_pump_time_announcement("The pump will occur in 5  MINS.")
