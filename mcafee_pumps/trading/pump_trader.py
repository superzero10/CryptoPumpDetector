from bittrex import Bittrex
from detection.bittrex_detector import BittrexService

BTC_TRADE_AMOUNT = 0.1
my_bittrex = Bittrex("a915c64c2fae4387ae569f0253ff5d67", "87ec1df1a1774886a342e26dcfdb9038")


def buy_limit(coin):
    print("TRADING...")
    bittrex_markets = BittrexService().fetch_btc_coin_data()['result']
    print(bittrex_markets)
    traded_coin = next((item for item in bittrex_markets if item['MarketName'] == coin))
    print(traded_coin)
    print(my_bittrex.buy_limit("BTC-LTC", 1.0, 0.0015))


buy_limit('BTC_LTC')
