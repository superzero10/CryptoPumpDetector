import time
import datetime
from detection.bittrex_service import BittrexService
from detection.constants import SERVER_REQUEST_FREQUENCY_SEC, MIN_BTC_VOLUME, MIN_SOAR_THRESHOLD
from detection.database_connection import obtain_db_connection

wanted_keys = {'MarketName', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders'}

bittrex_service = BittrexService()
active_btc_pairs = bittrex_service.fetch_active_btc_pairs()
new_coin_data = bittrex_service.fetch_coin_data()
db_connection = obtain_db_connection()
print(active_btc_pairs)

while True:
    time.sleep(SERVER_REQUEST_FREQUENCY_SEC)
    current_timestamp = time.time()
    current_time = datetime.datetime.now().time()

    coin_data = new_coin_data
    new_coin_data = bittrex_service.fetch_coin_data()
    for coin in new_coin_data['result']:
        if coin['BaseVolume'] >= MIN_BTC_VOLUME:
            old_coin = next((item for item in coin_data['result'] if item['MarketName'] == coin['MarketName']))
            # print(old_coin)
            if coin['Ask'] >= old_coin['Ask'] * MIN_SOAR_THRESHOLD:
                print('Possible pump coin: ', old_coin['MarketName'], ', was: ', old_coin['Ask'], ', is: ', coin['Ask'])

                unwanted_keys = set(coin.keys()) - wanted_keys
                for unwanted_key in unwanted_keys:
                    del coin[unwanted_key]

    print(current_time)

                # db_cursor = connection.cursor()
                # db_cursor.execute('SELECT * FROM COMPANY;')
                # rows = db_cursor.fetchall()
                # for row in rows:
                #     print(row[0], row[1], )2
