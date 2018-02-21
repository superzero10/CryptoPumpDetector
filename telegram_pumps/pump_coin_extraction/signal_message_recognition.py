import re


class PumpCoinExtractor:

    def extract_pump_signal(self, message_text):
        pass

    def extract_minutes_to_pump(self, message):
        message_text = message.lower()
        regex = r'\d+[" "]*["min"|"минут"]+'
        found_announcement = re.findall(regex, message_text)
        return self.__extract_minutes_to_pump(found_announcement)

    def __extract_minutes_to_pump(self, found_substrings):
        if not found_substrings:
            return None
        return ''.join((filter(str.isdigit, found_substrings[0])))


print(PumpCoinExtractor().extract_minutes_to_pump("POZOR!!123    минутwegtwb"))

