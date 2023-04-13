import requests
import json
from cur_bot_config_hidden import cur_dic, API_KEY


class ConvertionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f'Валюты совпадают {base}.')

        try:
            quote_tick = cur_dic[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_tick = cur_dic[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_tick}&from={base_tick}&amount={amount}"

        payload = {}
        headers = {
            "apikey": API_KEY
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        total_base = json.loads(r.content)
        total_base = total_base['result']
        total_base = round(total_base, 2)

        return total_base
