import time
import datetime
import requests


def crawl_bittrex():
    bittrex_market_response = requests.get(
        "https://bittrex.com/api/v1.1/public/getmarketsummaries")
    bittrex_coins_json = bittrex_market_response.json()
    print(bittrex_coins_json)
    return bittrex_coins_json


while True:
    print(datetime.datetime.now().time())
    print(time.time())
    time.sleep(5)

    crawl_bittrex()
