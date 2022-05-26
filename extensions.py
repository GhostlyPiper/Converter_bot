import requests
import json

from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:

    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(
                f'Невозможно перевести одинаковые валюты: < {base} >'
            )

        try:
            quote_ticker = keys[quote]

        except KeyError:
            raise ConvertionException(
                f'Не удалось обработать валюту: < {quote} >'
            )

        try:
            base_ticker = keys[base]

        except KeyError:
            raise ConvertionException(
                f'Не удалось обработать валюту: < {base} >'
            )

        try:
            amount = float(amount)

            if amount <= 0:
                raise ConvertionException(
                    f'Количество валюты должно быть положительным числом!'
                )

        except ValueError:
            raise ConvertionException(
                f'Не удалось обработать количество: < {amount} >'
            )

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        res = json.loads(r.content)[keys[base]]
        total_base = round(res * amount, 2)

        return total_base
