import time
import datetime
from detection.bittrex_service import BittrexService
from detection.constants import SERVER_REQUEST_FREQUENCY_SEC, MIN_BTC_VOLUME
from detection.database_connection import obtain_db_connection

wanted_keys = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}

service = BittrexService()
active_btc_pairs = service.fetch_active_btc_pairs()
new_coin_data = service.fetch_coin_data()
db_connection = obtain_db_connection()
print(active_btc_pairs)

while True:
    time.sleep(SERVER_REQUEST_FREQUENCY_SEC)
    print('current time is ' + str(time.time()))
    current_time = datetime.time()

    coin_data = new_coin_data
    new_coin_data = service.fetch_coin_data()
    for coin in new_coin_data["result"]:
        if not str(coin["MarketName"]).startswith('BTC') and not coin["BaseVolume"] >= MIN_BTC_VOLUME:
            print(coin)
            # print(coin["MarketName"] + ' {:.8f}'.format(coin["Ask"]))
            unwanted_keys = set(coin.keys()) - wanted_keys
            for unwanted_key in unwanted_keys:
                del coin[unwanted_key]
            print(coin)

    print('')

    # db_cursor = connection.cursor()
    # db_cursor.execute('SELECT * FROM COMPANY;')
    # rows = db_cursor.fetchall()
    # for row in rows:
    #     print(row[0], row[1], )2
