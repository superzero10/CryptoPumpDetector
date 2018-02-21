import re


class PumpCoinExtractor:

    def extract_pump_signal(self, message_text):
        pass

    def extract_minutes_to_pump(self, message_text):
        normalized_message_text = message_text.lower().strip()

        if normalized_message_text.isdigit():
            return normalized_message_text  # some groups like countdown using messages which contain only the minutes
        else:
            return self.__find_minutes_to_pump(normalized_message_text)

    def __find_minutes_to_pump(self, message):
        regex = r'\d+[" "]*min|минут'
        found_substrings = re.findall(regex, message)
        if not found_substrings:
            return None
        return ''.join((filter(str.isdigit, found_substrings[0])))


print(PumpCoinExtractor().extract_minutes_to_pump("Two. Minutes. 30 minutes to the pump"))

