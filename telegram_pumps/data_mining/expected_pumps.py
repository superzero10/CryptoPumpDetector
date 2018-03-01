from time import time


class ExpectedPumpsHandler:
    _expected_pump_timestamps = {}  # (group_id, timestamp)
    _expected_pump_exchanges = {}  # (group_id, dict{ex1, ex2, ex3])

    _sec_epsilon = 30
    _exchange_names = ['yobit', 'coinexchange', 'cryptopia', 'binance']

    def save_expected_pump_time_if_present(self, group_id, minutes_to_pump):
        if minutes_to_pump:
            print('FOUND PUMP ANNOUNCEMENT: ', minutes_to_pump, ' MINUTES TO PUMP\n')
            self._expected_pump_timestamps.pop(group_id, None)
            self._expected_pump_timestamps[group_id] = time() + minutes_to_pump * 60
            print('EXPECTED PUMPS SET: ', self._expected_pump_timestamps)

    def save_expected_pump_exchange_if_present(self, group_id, exchange_name):
        if exchange_name:
            self._expected_pump_exchanges.pop(group_id, None)
            self._expected_pump_exchanges[group_id] = exchange_name
            print('FOUND PUMP EXCHANGE: ', exchange_name, '\n')

    def is_within_expected_pump_date_range(self, group_id):
        expected_pump_time = self._expected_pump_timestamps.get(group_id, None)
        current_time = time()
        if expected_pump_time:
            return expected_pump_time - self._sec_epsilon <= current_time <= expected_pump_time + self._sec_epsilon
        else:
            return False

    def delete_obsolete_expected_pump_timestamps(self):
        current_time = time()
        print('\nsearching for and deleting obsolete expected pumps, current time is: ', current_time, "\n")

        for channel_id, expected_timestamp in self._expected_pump_timestamps.items():
            if expected_timestamp + self._sec_epsilon < current_time:
                del self._expected_pump_timestamps[channel_id]
                print('deleted obsolete expected pump, new state is: ', self._expected_pump_timestamps)
