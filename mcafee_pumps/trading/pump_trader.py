import threading
import time

from exchange_services.bittrex_wrapper import Bittrex, TIMEINEFFECT_IMMEDIATE_OR_CANCEL, ORDERTYPE_MARKET, \
    TIMEINEFFECT_GOOD_TIL_CANCELLED, ORDERTYPE_LIMIT

BTC_PREFIX = "BTC-"
BTC_TRADE_SIZE = 0.05
bittrex_trader = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")


def trade_market(coin):
    print('MARKET TRADE ', coin)

    # buy_thread = threading.Thread(target=_buy(coin))
    # buy_thread.start()
    # sell_thread = threading.Thread(target=_sell(coin))
    # sell_thread.start()


def _buy(coin_symbol):
    market_name = BTC_PREFIX + coin_symbol
    print('Buy thread started')
    start_time = time.time()
    coin_price_response = bittrex_trader.get_marketsummary(market_name)
    if coin_price_response['result']['MarketName'] == coin_symbol:
        last_coin_ask_price = coin_price_response['result']['Ask']
        print(coin_price_response)
        print('Last Ask', last_coin_ask_price)
        buy_order_response = bittrex_trader.trade_buy(market=market_name, order_type=ORDERTYPE_LIMIT,
                                                      time_in_effect=TIMEINEFFECT_GOOD_TIL_CANCELLED, quantity=1, rate=0.001)
        print('Buy order: ', buy_order_response)
        print('buy request took', time.time() - start_time, ' seconds')


def _sell(coin_symbol):
    market_name = BTC_PREFIX + coin_symbol
    print('Sell thread started')
    time.sleep(10)
    bought_amount_response = bittrex_trader.get_balance(currency=coin_symbol)
    print('CURRENCY BALANCE RESPONSE', bought_amount_response)
    print('Selling now..')
    sell_quantity = bought_amount_response['result']['Available']
    sell_order_response = bittrex_trader.trade_sell(market=market_name,
                                                    order_type=ORDERTYPE_LIMIT,
                                                    time_in_effect=TIMEINEFFECT_GOOD_TIL_CANCELLED,
                                                    quantity=sell_quantity)
    print('Sell order: ', sell_order_response)
