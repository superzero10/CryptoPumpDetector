import time

from psycopg2._json import Json
from common.database.database_connection import obtain_db_connection
from mcafee_pumps.image_evaluation.words_api_service import fetch_word_definitions_count

COIN_SUFFIX = 'coin'
WORD_VALUE_DENOMINATOR = 35
FORBIDDEN_PART_WORDS = ['Breakout', 'Ethereum', 'Internet', 'Basic', 'Status', 'Bitcoin', 'Project']


def create_coin_keywords_eval_dict():
    market_names_list = BittrexService().fetch_active_btc_pairs_with_names()
    db_connection = obtain_db_connection()
    markets_eval_dict = []

    for market in market_names_list:

        # create different permutations of the coin names that are plausible to be used in the tweeted image
        if market[1].lower().endswith(COIN_SUFFIX):
            potential_coin_variant = market[1][:-4].lower().capitalize()
            if len(potential_coin_variant) > 1 and market[1].lower() != potential_coin_variant.lower() and \
                    potential_coin_variant not in FORBIDDEN_PART_WORDS:
                market.append(potential_coin_variant)

        if len(market[1].split(' ')) > 1:
            potential_coin_variant = market[1].split(' ')[0]
            if potential_coin_variant not in FORBIDDEN_PART_WORDS:
                market.append(potential_coin_variant)

        if market[0].lower() == market[-1].lower():
            del market[-1]

        # convert to definition count punishment partial dictionary
        current_market_dictionary = []
        for index, market_alias in enumerate(market):
            print(index, market_alias)
            if market_alias.lower().endswith(COIN_SUFFIX):
                # coins with names "*coin" are definitely not proper english words
                current_market_coin_tuple = (market_alias, 1)
            else:
                # calculate the word trust value depending on english dictionary definitions count
                current_market_word_value = 1 - fetch_word_definitions_count(market_alias) / WORD_VALUE_DENOMINATOR
                current_market_coin_tuple = (market_alias, current_market_word_value)
            current_market_dictionary.append(current_market_coin_tuple)
        print("Punishment dictionary for current coin: ", current_market_dictionary)
        print("")

        markets_eval_dict.append(current_market_dictionary)

    print(markets_eval_dict)

    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT into coins (timestamp, dict) values (%s, %s)',
                      [time.time(), Json(markets_eval_dict)])
    db_connection.commit()
    db_connection.close()


def fetch_word_evaluation_dictionary():
    db_connection = obtain_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT dict FROM coins')
    word_eval_dict = db_cursor.fetchone()
    db_connection.close()
    return word_eval_dict[0]


id_list = [1173818556,
           1214662212,
           1317772193,
           1263077730,
           1291394110,
           1089342938,
           1271617066,
           1241060482,
           1357346989,
           1250236348,
           1216349468,
           1264269735,
           1252587866,
           1168820453,
           1273394342,
           1279231032,
           1150841156,
           1164231494,
           1239731459,
           1374296459,
           1334377716,
           1334478809,
           1281858086,
           1354898965,
           1242306021,
           1291921757,
           1392633745,
           1138352002,
           1192449498,
           1168448346,
           1341240918,
           1128106243,
           1243063350,
           1198067789,
           1176512969,
           1309310305,
           1121116526,
           1181666936,
           1200431729,
           1382526245,
           1231984200,
           1228587735,
           1282766017,
           1263889558,
           1228528937,
           1359570723,
           1188607041,
           1363328213,
           1328793376,
           1247370590,
           1190316874,
           1341820294,
           1130353104,
           1269980463,
           1220655817,
           1377799373,
           1397561227,
           1277335084,
           1297239210,
           1369360011,
           1139185736,
           1186808784,
           1155866782,
           1350503556,
           1299161063,
           1148932045,
           1379711908,
           1133951784,
           1245572836,
           1213347273,
           1189228308,
           1259502930,
           1128884686,
           1233262804,
           1364833277,
           1266276750,
           1335283603,
           1351149495,
           1316961309,
           1255036492,
           1189711995,
           1184763128,
           1377636832,
           1374709721,
           1146981875,
           1302710231,
           1200431729,
           1280049674,
           1361178294]

name_list = ['Yobit-2ch-Pumper',
             'PUMPROCKET',
             'Pump Coin',
             'RUSSIA PUMP',
             'TOP PUMP VIP',
             'CANADA PUMP',
             'REDdBULL PUMP',
             'Alt Pump Cryptopia',
             'Pumpimm',
             'Big pump to the moon',
             'PUMPINATOR',
             'Rocket pump',
             'TO THE MOON',
             'RedMoon Pump',
             'PumpFather',
             'Gold PUMP',
             'Crypto Mafia Channel',
             'PUMP Men',
             'Trust PUMP',
             'NAMN KAHAN PUMP',
             'Spartan Pumps',
             'Big Pump Signal',
             'Crypto pumpers',
             'Capitan Pump',
             'CryptonianPumpers',
             'Binance Pump',
             'Crypto Kings Pump',
             'Crypto Poppers',
             'BEST PUMP',
             'GOLDEN DRAGON PUMPS',
             'YOBIT_PUMP + ...',
             'Pump YObit.net',
             'PUMP-JOCKER',
             'PumpWhales',
             'Altcoin Pumpers Picks',
             'PUMP&DUMASS',
             'Crypto Callz 2.0',
             'Namn mohntopnhr',
             'NAMN KAHAN YOBIT',
             'SuperPump',
             'NAMN n PAMN',
             'FriendlyPump',
             'ALL PUMPS',
             'Public Pump&Dump',
             'CRYPTO PUMPS',
             'PumpLab',
             'CryptoPiaPump',
             'YObit Pump Network',
             'Pump Squad Royale',
             'Pump To The Moon',
             'Bit-pump_pro',
             'Fenix Pump',
             'Superb Pumps',
             'Pump & Gain',
             'Big Russian PUMP',
             'MoneyLuck',
             'SuperPump',
             'Crypto Pump',
             'Mega Pump Group',
             'GosPump',
             'NAMN/PUMP',
             'CRYPTO EAGLE',
             'Pro Pump',
             'Crypto pumps india',
             'Namnbi kpntobankot',
             'Trump Pump',
             'Pumproom',
             'CoinExchange (Pumps)',
             'Scrooge McPump',
             'ROCKET PUMP GROUP',
             'World Best Crypto Pumps',
             'Underground Pumps',
             'Alt the Way',
             'Team Pumps',
             'Pablo Pumps',
             'JumpinJack',
             'YoubitPump & Hoboctn',
             'PUMP AND BOOM CRYPTO',
             'Explosive Pumps',
             'The Kings of Pump',
             'Super Pumps',
             'Bitcoin Pumps',
             'YoBit-Pump-Community',
             'INSANE PUMPS',
             'NAMN KAHAN YOBIT',
             'BEpump',
             'ProfitMoon - Namn',
             'Really pump_yo',
             'Cryptopia Pump']

types_list = ['image',
              'image',
              'text',
              'text',
              'text',
              'text',
              'unknown',
              'unknown',
              'text',
              'text',
              'unknown',
              'image',
              'image',
              'unknown',
              'unknown',
              'unknown',
              'text',
              'image',
              'text',
              'image',
              'text',
              'text',
              'text',
              'image',
              'text',
              'unknown',
              'unknown',
              'text',
              'text',
              'unknown',
              'unknown',
              'unknown',
              'image',
              'unknown',
              'text',
              'text',
              'unknown',
              'unknown',
              'unknown',
              'image',
              'image',
              'text',
              'unknown',
              'text',
              'text',
              'image',
              'unknown',
              'unknown',
              'text',
              'image',
              'text',
              'text',
              'text',
              'text',
              'text',
              'image',
              'unknown',
              'text',
              'image',
              'text',
              'unknown',
              'image',
              'text',
              'text',
              'text',
              'text',
              'text',
              'unknown',
              'image',
              'image',
              'text',
              'text',
              'text',
              'text',
              'text',
              'text',
              'image',
              'text',
              'text',
              'unknown',
              'unknown',
              'text',
              'image',
              'text',
              'image',
              'text',
              'unknown',
              'text',
              'unknown']


def save_to_db():
    db_connection = obtain_db_connection()
    db_cursor = db_connection.cursor()

    for index in range(0, len(id_list)):
        db_cursor.execute('INSERT into pump_groups (group_id, name, signal_type) values (%s, %s, %s)',
                          [id_list[index], name_list[index], types_list[index]])

    db_connection.commit()
    db_connection.close()


save_to_db()
