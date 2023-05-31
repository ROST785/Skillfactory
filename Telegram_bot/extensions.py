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
            value1_ticker = keys[value1]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {value1}")

        try:
            value2_ticker = keys[value2]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {value2}")

        try:
            count = float(count)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {count}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={value1_ticker}&tsyms={value2_ticker}")
        total_value2 = round(json.loads(r.content)[keys[value2]] * count, 3)

        return total_value2