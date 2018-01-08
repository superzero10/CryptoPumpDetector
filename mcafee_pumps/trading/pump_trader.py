import threading
import time

from exchange_services.bittrex_wrapper import Bittrex, TIMEINEFFECT_IMMEDIATE_OR_CANCEL, ORDERTYPE_MARKET, \
    TIMEINEFFECT_GOOD_TIL_CANCELLED

BTC_PREFIX = "BTC-"
bittrex_trader = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")


def trade_market(coin):
    pair_symbol = BTC_PREFIX + coin.upper()
    print('MARKET TRADE ', pair_symbol)

    buy_thread = threading.Thread(target=_buy(pair_symbol))
    buy_thread.start()
    sell_thread = threading.Thread(target=_sell(pair_symbol))
    sell_thread.start()


def _buy(pair_symbol):
    print('Buy thread started')
    start_time = time.time()
    buy_order_response = bittrex_trader.trade_buy(market=pair_symbol, order_type=ORDERTYPE_MARKET,
                                                  time_in_effect=TIMEINEFFECT_IMMEDIATE_OR_CANCEL, quantity=0.01)
    print('Buy order: ', buy_order_response)
    uuid = buy_order_response['result']['uuid']
    print('buy request took', time.time() - start_time, ' seconds')


def _sell(pair_symbol):
    print('Sell thread started')
    time.sleep(15)
    bought_amount_response = bittrex_trader.get_balance(currency=pair_symbol)
    print('CURRENCY BALANCE RESPONSE', bought_amount_response)
    print('Selling now..')
    sell_order_response = bittrex_trader.trade_sell(market=pair_symbol, order_type=ORDERTYPE_MARKET,
                                                    time_in_effect=TIMEINEFFECT_GOOD_TIL_CANCELLED, quantity=0.01)
    print('Sell order: ', sell_order_response)
