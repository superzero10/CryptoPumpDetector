import time

from detection.bittrex_cron_crawler import crawl_bittrex, crawl_active_btc_pairs
from detection.constants import SERVER_SCRAPPING_FREQUENCY_SEC, MIN_BTC_VOLUME
from detection.database_connection import connect_to_database

coin_data = crawl_bittrex()
active_coins_names = crawl_active_btc_pairs()
connect_to_database()
print(active_coins_names)

while True:
    time.sleep(SERVER_SCRAPPING_FREQUENCY_SEC)
    print('current time is ' + str(time.time()))

    coin_data = crawl_bittrex()
    for coin in coin_data["result"]:
        if str(coin["MarketName"]).startswith('BTC') and coin["BaseVolume"] >= MIN_BTC_VOLUME:
            print(coin["MarketName"] + ' {:.8f}'.format(coin["Ask"]))

    print('')
