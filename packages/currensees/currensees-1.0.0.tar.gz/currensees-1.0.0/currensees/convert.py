import requests

class CurrenseesConvert:
    def __init__(self, base_url):
        self.base_url = base_url

    def convert(self, date, base_currency, target_currency, amount):
        url = f"{self.base_url}/convert"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        data = {
            'date': date,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'amount': amount,
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
