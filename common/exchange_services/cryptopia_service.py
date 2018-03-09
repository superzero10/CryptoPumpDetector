import requests


class CryptopiaService:
    _RESULT = 'Data'
    _COIN_NAME = 'Symbol'

    def fetch_active_btc_pairs(self):
        active_pairs_response = requests.get("https://www.cryptopia.co.nz/api/GetCurrencies").json()
        active_pairs_data = active_pairs_response[self._RESULT]
        coin_symbols = [coin[self._COIN_NAME].lower() for coin in active_pairs_data]
        return coin_symbols


CryptopiaService().fetch_active_btc_pairs()
