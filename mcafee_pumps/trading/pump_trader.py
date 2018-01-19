import time

from common.exchange_services import Bittrex

BTC_PREFIX = "BTC-"
BTC_TRADE_SIZE = 0.0025
bittrex_trader = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")
BUY_OVERSHOOT = 1.1


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
    if coin_price_response['result'][0]['MarketName'] == market_name:
        last_ask_price = coin_price_response['result'][0]['Ask']
        print(coin_price_response)
        print('Last Ask', last_ask_price)

        buy_quantity = BTC_TRADE_SIZE / (last_ask_price * BUY_OVERSHOOT)
        print('Buy quantity: ', buy_quantity)

        buy_order_response = bittrex_trader.buy_limit(market=market_name, quantity=buy_quantity, rate=last_ask_price * BUY_OVERSHOOT)
        print('Buy order: ', buy_order_response)
        print('buy request took', time.time() - start_time, ' seconds')

        # cancel the request if not successful
        uuid = buy_order_response['result']['uuid']
        time.sleep(4)
        cancel_response = bittrex_trader.cancel(uuid)
        print('Buy request cancel response: ', cancel_response)


def _sell(coin_symbol):
    market_name = BTC_PREFIX + coin_symbol
    print('Sell thread started')
    time.sleep(14)
    bought_amount_response = bittrex_trader.get_balance(currency=coin_symbol)
    print('CURRENCY BALANCE RESPONSE', bought_amount_response)
    print('Selling now..')
    sell_quantity = bought_amount_response['result']['Available']

    coin_price_response = bittrex_trader.get_marketsummary(market_name)

    if coin_price_response['result'][0]['MarketName'] == market_name:
        last_ask_price = coin_price_response['result'][0]['Ask']
        print(coin_price_response)
        print('Last Ask', last_ask_price)

        sell_order_response = bittrex_trader.sell_limit(market=market_name, quantity=sell_quantity, rate=last_ask_price)
        print('Sell order: ', sell_order_response)
