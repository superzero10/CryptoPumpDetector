from mcafee_pumps.detection.coin_dictionary import fetch_word_evaluation_dictionary

word_eval_dict = fetch_word_evaluation_dictionary()
print(word_eval_dict)
print('')


def extract_mentioned_coin_abbr(text):
    coin_name_occurences = {}

    for coin_name_variants in word_eval_dict:
        print(coin_name_variants)
        for coin_name_trust_value in coin_name_variants:
            coin_name_variant = coin_name_trust_value[0]
            print()


extract_mentioned_coin_abbr("""A powerhouse platform being applied to a
wide range of fields. FCT has been endorsed
by the Bill Gates Foundation and Homeland
Security has a fully implemented technology
China. It is one the few Blockchain
and already has contracts with 25 cities in
companies with a fully functional API that
integrates directly with most existing software,
allowing sharing, auditing and exchange of a
wide range of sensitive documents. FACTOM.
COM.""")
