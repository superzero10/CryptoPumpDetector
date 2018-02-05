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


# def save_to_db():
#     db_connection = obtain_db_connection()
#     db_cursor = db_connection.cursor()
#
#     for index in range(0, len(id_list)):
#         db_cursor.execute('INSERT into pump_groups (group_id, name, signal_type) values (%s, %s, %s)',
#                           [id_list[index], name_list[index], types_list[index]])
#
#     db_connection.commit()
#     db_connection.close()
#
#
# save_to_db()
