
from mcafee_pumps.evaluation.words_api_evaluator import fetch_word_definitions_count
from exchange_services.bittrex_service import BittrexService


def create_coin_keywords_eval_dict():
    base_coin_names_list = BittrexService().fetch_active_btc_pairs_with_names()
    print(base_coin_names_list)
    #
    # if market[MARKET_LONG_NAME] != market[MARKET_LONG_NAME].capitalize():
    #             market_name_variants_list.append(market[MARKET_LONG_NAME].capitalize())
    #
    #         if market[MARKET_LONG_NAME].lower().endswith("coin"):
    #             market_name_variants_list.append(market[MARKET_LONG_NAME][:-4])


create_coin_keywords_eval_dict()