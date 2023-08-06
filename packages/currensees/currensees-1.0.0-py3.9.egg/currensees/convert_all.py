import requests

class CurrenseesConvertAll:
    def __init__(self, base_url):
        self.base_url = base_url

    def convert_all(self, base_currency, amount, date):
        url = f"{self.base_url}/convert_all"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        data = {
            'base_currency': base_currency,
            'amount': amount,
            'date': date,
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
