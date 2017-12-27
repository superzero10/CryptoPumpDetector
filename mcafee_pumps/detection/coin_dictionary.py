from mcafee_pumps.evaluation.words_api_evaluator import fetch_word_definitions_count
from exchange_services.bittrex_service import BittrexService
import itertools


def create_coin_keywords_eval_dict():
    market_names_list = BittrexService().fetch_active_btc_pairs_with_names()
    markets_eval_dict = {}

    for market in market_names_list:

        # create different permutations of the coin names that are plausible to be used
        if market[1] != market[1].capitalize():
            market.append(market[1].capitalize())
        if market[1].lower().endswith('coin'):
            market.append(market[1][:-4].lower().capitalize())
        if market[0] == market[1]:
            del market[1]

        # convert to definition count punishment partial dictionary
        current_market_dictionary = {}
        for index, item in enumerate(market):
            print(index, item)
            if index is 0 or item.endswith('coin'):
                # cannot punish coin names, and coins with names "*coin" are definitely not proper english words
                current_market_update_dict = {item: 0}
            else:
                current_market_update_dict = {item: fetch_word_definitions_count(item)}
            current_market_dictionary.update(current_market_update_dict)
        print("Punishment dictionary for current coin: ", current_market_dictionary)
        print("")

        markets_eval_dict.update(current_market_dictionary)

    print(markets_eval_dict)


create_coin_keywords_eval_dict()
