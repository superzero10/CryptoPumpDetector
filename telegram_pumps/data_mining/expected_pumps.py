from datetime import datetime
from threading import Lock
from time import time


class ExpectedPumpsHandler:
    _expected_pump_timestamps = {}  # (group_id, timestamp)
    _expected_pump_exchanges = {}  # (group_id, dict{ex1, ex2, ex3])
    _lock = Lock()

    _sec_epsilon = 60
    _exchange_names = ['yobit', 'coinexchange', 'cryptopia', 'binance']

    def save_expected_pump_time_if_present(self, group_id, minutes_to_pump):
        if minutes_to_pump:
            with self._lock:
                self.__delete_obsolete_expected_pump_timestamps()
                print('FOUND PUMP ANNOUNCEMENT: ', minutes_to_pump, ' MINUTES TO PUMP\n')
                self._expected_pump_timestamps.pop(group_id, None)
                self._expected_pump_timestamps[group_id] = time() + minutes_to_pump * 60
                print('EXPECTED PUMPS SET: ', self._expected_pump_timestamps)

    def __delete_obsolete_expected_pump_timestamps(self):
        current_time = time()
        print('\nsearching for and deleting obsolete expected pumps, current time is: ', current_time, "\n")

        for channel_id, expected_timestamp in self._expected_pump_timestamps.items():
            if expected_timestamp + self._sec_epsilon < current_time:
                del self._expected_pump_timestamps[channel_id]
                print('deleted obsolete expected pump, new state is: ', self._expected_pump_timestamps)

    def save_expected_pump_exchange_if_present(self, group_id, exchange_name):
        if exchange_name:
            with self._lock:
                self._expected_pump_exchanges.pop(group_id, None)
                self._expected_pump_exchanges[group_id] = exchange_name
                print('FOUND PUMP EXCHANGE: ', exchange_name, '\n')

    def is_within_expected_pump_date_range(self, group_id):
        with self._lock:
            expected_pump_time = self._expected_pump_timestamps.get(group_id, None)
            current_time = time()
            if expected_pump_time:
                result = expected_pump_time - self._sec_epsilon <= current_time <= expected_pump_time + self._sec_epsilon

                if result:
                    expected_lower_range_date = datetime.utcfromtimestamp(
                        self._expected_pump_timestamps[group_id] - self._sec_epsilon).strftime(
                        "%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
                    expected_higher_range_date = datetime.utcfromtimestamp(
                        self._expected_pump_timestamps[group_id] + self._sec_epsilon).strftime(
                        "%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")

                    print('|||||||||| PUMP DETECTED, expected time was',
                          expected_lower_range_date, '-', expected_higher_range_date, 'actual time ',
                          datetime.utcfromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)"))

                return result
            else:
                return False
