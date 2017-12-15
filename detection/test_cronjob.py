import time
import requests


def crawl_bittrex():
    bittrex_market_response = requests.get(
        "https://bittrex.com/api/v1.1/public/getmarketsummaries")
    return bittrex_market_response.json()


while True:
    print('current time is ' + str(time.time()))

    for coin in crawl_bittrex()["result"]:
        if str(coin["MarketName"]).startswith('BTC'):
            print(coin["MarketName"] + ' {:.8f}'.format(coin["Last"]))

    print('')
    time.sleep(2)
