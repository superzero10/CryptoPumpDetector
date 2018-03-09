from YoBit import YoBit

yobit = YoBit(api_key='958381B7C507CD2A504C9FF2C629EAA1', api_secret='5711a46ae0855fa27a9f8b45e368b931')


def fetch_yobit_pairs():
    return list(yobit.info()['pairs'].keys())


def fetch_yobit_coins():
    pairs = fetch_yobit_pairs()
    coins = [str(pair).split('_')[0] for pair in pairs]
    coins_set = set(coins)
    return coins_set


if __name__ == '__main__':
    fetch_yobit_coins()
