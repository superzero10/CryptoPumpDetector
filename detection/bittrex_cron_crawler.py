import requests


def crawl_bittrex():
    bittrex_market_response = requests.get(
        "https://bittrex.com/api/v1.1/public/getmarketsummaries")
    print(bittrex_market_response)
    return bittrex_market_response.json()


def crawl_active_btc_pairs():
    coin_list = []
    coin_data = crawl_bittrex()
    for coin in coin_data["result"]:
        if str(coin["MarketName"]).startswith('BTC'):
            coin_list.append(coin["MarketName"])

    return coin_list
