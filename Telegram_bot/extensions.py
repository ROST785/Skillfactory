import requests
import json
from config import keys


class APIException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def get_price(value1, value2, count):
        if value1 == value2:
            raise APIException(f"Невозможно перевести одинаковые валюты {value1}")

        try:
            value1_ticker = keys[value1.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {value1}")

        try:
            value2_ticker = keys[value2.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {value2}")

        try:
            count = float(count)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {count}")

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={value1_ticker}&symbols={value2_ticker}")
        resp = json.loads(r.content)
        total_value2 = resp['rates'][keys[value2]] * count

        return total_value2