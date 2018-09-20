from datetime import datetime
from threading import Lock
from time import time


class ExpectedPumpsHandler:
    _expected_pump_timestamps = {}  # (group_id, timestamp)
    _expected_pump_exchanges = {}  # (group_id, dict{ex1, ex2, ex3])
    _lock = Lock()

    epsilon = 70  # in seconds
    _exchange_names = ['yobit', 'coinexchange', 'cryptopia', 'binance']

    def save_expected_pump_time_if_present(self, group_id, minutes_to_pump):
        if minutes_to_pump:
            with self._lock:
                self.__delete_obsolete_expected_pump_timestamps()
                self._expected_pump_timestamps.pop(group_id, None)
                self._expected_pump_timestamps[group_id] = time() + minutes_to_pump * 60

    def __delete_obsolete_expected_pump_timestamps(self):
        current_time = time()

        for channel_id in list(self._expected_pump_timestamps):
            if self._expected_pump_timestamps[channel_id] + self.epsilon < current_time:
                self._expected_pump_timestamps.pop(channel_id, None)

    def save_expected_pump_exchange_if_present(self, group_id, exchange_name):
        if exchange_name:
            with self._lock:
                self._expected_pump_exchanges.pop(group_id, None)
                self._expected_pump_exchanges[group_id] = exchange_name

    def is_within_expected_pump_date_range(self, group_id):
        with self._lock:
            expected_pump_time = self._expected_pump_timestamps.get(group_id, None)
            current_time = time()
            if expected_pump_time:
                result = expected_pump_time - self.epsilon <= current_time <= expected_pump_time + self.epsilon

                if result:
                    expected_lower_range_date = datetime.utcfromtimestamp(
                        self._expected_pump_timestamps[group_id] - self.epsilon).strftime("%H:%M:%S.%f+00:00 (UTC)")
                    expected_higher_range_date = datetime.utcfromtimestamp(
                        self._expected_pump_timestamps[group_id] + self.epsilon).strftime("%H:%M:%S.%f+00:00 (UTC)")

                    print(datetime.time(datetime.now()), '|||||||||| PUMP DETECTED, expected time was',
                          expected_lower_range_date, '-', expected_higher_range_date, 'actual time ',
                          datetime.utcfromtimestamp(current_time).strftime("%H:%M:%S.%f+00:00 (UTC)"))

                return result
            else:
                return False

    def get_expected_exchange(self, group_id):
        return self._expected_pump_exchanges.pop(group_id, None)
