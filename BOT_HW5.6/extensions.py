import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f'https://v6.exchangerate-api.com/v6/3033232cf8110ca750c3eaaa/latest/{base}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException(f'Ошибка получения данных от API: {response.status_code}')

        data = response.json()

        if quote not in data['conversion_rates']:
            raise APIException(f'Валюта {quote} не найдена.')

        rate = data['conversion_rates'][quote]
        return rate * amount