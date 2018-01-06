import time

from detection.bittrex_detector import BittrexService
from exchange_services.bittrex_wrapper import Bittrex

BTC_TRADE_AMOUNT = 0.1
bittrex_trader = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")


def buy_limit(coin):
    while True:
        print("TRADING...")
        time.sleep(10)
        start_time = time.time()
        # print(bittrex_trader.get_balance("BTC"))

        place_order_response = bittrex_trader.buy_limit('BTC-LTC', 1, 0.001)
        print('Place order: ', place_order_response)
        uuid = place_order_response['result']['uuid']
        print('trade request took', time.time() - start_time)

        cancel_order_response = bittrex_trader.cancel(uuid)
        print('Cancel order: ', cancel_order_response)


# buy_limit('BTC_LTC')
