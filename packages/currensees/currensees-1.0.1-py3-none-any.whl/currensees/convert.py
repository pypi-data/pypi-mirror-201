import requests
import json

class CurrencyConverter:
    def __init__(self, base_currency, target_currency, amount, date):
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.amount = amount
        self.date = date

    def convert(self):
        url = "https://currensees.com/v1/convert"

        payload = json.dumps({
            "date": self.date,
            "base_currency": self.base_currency,
            "target_currency": self.target_currency,
            "amount": self.amount
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
