import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Введена несуществующая валюта {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Введена несуществующая валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введено несуществующее число {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total = float(amount) * json.loads(r.content)[keys[base]]
        
        return total
