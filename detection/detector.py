import time

from detection.bittrex_cron_crawler import crawl_bittrex, crawl_active_btc_pairs
from detection.constants import SERVER_SCRAPPING_FREQUENCY_SEC

coin_data = crawl_bittrex()
active_coin_names = crawl_active_btc_pairs()
print(active_coin_names)

while True:
    time.sleep(SERVER_SCRAPPING_FREQUENCY_SEC)
    print('current time is ' + str(time.time()))

    coin_data = crawl_bittrex()
    for coin in coin_data["result"]:
        if str(coin["MarketName"]).startswith('BTC'):
            print(coin["MarketName"] + ' {:.8f}'.format(coin["Last"]))

    print('')
