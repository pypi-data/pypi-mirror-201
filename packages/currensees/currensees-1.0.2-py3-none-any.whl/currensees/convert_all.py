import requests
import json

class ConvertAllCurrencies:
    def __init__(self, base_currency, amount, date):
        self.base_currency = base_currency
        self.amount = amount
        self.date = date

    def convert(self):
        url = "https://currensees.com/v1/convert_all"

        payload = json.dumps({
            "base_currency": self.base_currency,
            "amount": self.amount,
            "date": self.date
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
