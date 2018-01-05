import time

from psycopg2._json import Json

from database.database_connection import obtain_db_connection
from exchange_services.bittrex_service import BittrexService
from mcafee_pumps.evaluation.words_api_evaluator import fetch_word_definitions_count

COIN_SUFFIX = 'coin'


def create_coin_keywords_eval_dict():
    market_names_list = BittrexService().fetch_active_btc_pairs_with_names()
    db_connection = obtain_db_connection()
    markets_eval_dict = {}

    for market in market_names_list[:3]:

        # create different permutations of the coin names that are plausible to be used in the tweeted image
        if market[1] != market[1].capitalize():
            market.append(market[1].capitalize())
        if market[1].lower().endswith(COIN_SUFFIX):
            market.append(market[1][:-4].lower().capitalize())
        if market[0] == market[1]:
            del market[1]

        # convert to definition count punishment partial dictionary
        current_market_dictionary = {}
        for index, market_alias in enumerate(market):
            print(index, market_alias)
            if index is 0 or market_alias.lower().endswith(COIN_SUFFIX):
                # cannot punish coin names. also coins with names "*coin" are definitely not proper english words
                current_market_dict_update = {market_alias: 1}
            else:
                current_market_dict_update = {market_alias: fetch_word_definitions_count(market_alias)}
            current_market_dictionary.update(current_market_dict_update)
        print("Punishment dictionary for current coin: ", current_market_dictionary)
        print("")

        markets_eval_dict.update(current_market_dictionary)

    print(markets_eval_dict)

    db_cursor = db_connection.cursor()
    db_cursor.execute('INSERT into coins (timestamp, dict) values (%s, %s)',
                      [time.time(), Json(markets_eval_dict)])
    db_connection.commit()
    db_connection.close()


create_coin_keywords_eval_dict()
