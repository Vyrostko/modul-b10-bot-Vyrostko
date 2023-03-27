import requests
import json

from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_prise(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        headers= {
        "apikey": "7uImkqZdlPwNiV57yd4YCbyIV4KMsz7Q"
        }
        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}", headers=headers)
        resp = json.loads(r.content)
        new_price = resp['rates'][exchanges[quote_key]] * amount
        new_price = round(new_price, 3)
        return new_price
