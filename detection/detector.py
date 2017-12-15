import time

from detection.bittrex_cron_crawler import BittrexCrawler

coin_data = BittrexCrawler.crawl_bittrex()
active_coin_names = BittrexCrawler.crawl_active_btc_pairs()
print(active_coin_names)

while True:
    time.sleep(15)
    print('current time is ' + str(time.time()))

    coin_data = BittrexCrawler.crawl_bittrex()
    for coin in coin_data["result"]:
        if str(coin["MarketName"]).startswith('BTC'):
            print(coin["MarketName"] + ' {:.8f}'.format(coin["Last"]))

    print('')
