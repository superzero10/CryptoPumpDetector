from mcafee_pumps.detection.coin_dictionary import fetch_word_evaluation_dictionary

word_eval_dict = fetch_word_evaluation_dictionary()
print(word_eval_dict)
print('')


def extract_mentioned_coin_abbr(text):
    coin_name_occurences = {}

    for coin_name_variants in word_eval_dict:
        for coin_value_tuple in coin_name_variants:
            coin_name = coin_value_tuple[0].lower()
            if count_occurrences(coin_name, text) > 0:
                print(coin_name.upper(), ' found ', count_occurrences(coin_name, text), ' times at value ', coin_value_tuple[1])


def count_occurrences(word, text):
    return text.lower().count(word)


extract_mentioned_coin_abbr("""FACTOM (FCT) 
A powerhouse platform being applied to a
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
