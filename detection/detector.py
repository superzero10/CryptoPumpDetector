import time

from detection.bittrex_service import BittrexService
from detection.constants import SERVER_SCRAPPING_FREQUENCY_SEC, MIN_BTC_VOLUME
from detection.database_connection import obtain_db_connection

service = BittrexService()
active_btc_pairs = service.fetch_active_btc_pairs()
obtain_db_connection()
print(active_btc_pairs)

while True:
    time.sleep(SERVER_SCRAPPING_FREQUENCY_SEC)
    print('current time is ' + str(time.time()))

    coin_data = service.fetch_coin_data()
    for coin in coin_data["result"]:
        if str(coin["MarketName"]).startswith('BTC') and coin["BaseVolume"] >= MIN_BTC_VOLUME:
            print(coin["MarketName"] + ' {:.8f}'.format(coin["Ask"]))

    print('')
