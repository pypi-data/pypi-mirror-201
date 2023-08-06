import requests

class Currencies:
    def __init__(self, username, day, month, year):
        self.username = username
        self.day = day
        self.month = month
        self.year = year

    def get_currencies(self):
        url = f"https://currensees.com/v1/currencies?username={self.username}&day={self.day}&month={self.month}&year={self.year}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def get_currency_by_uuid(self, uuid):
        url = f"https://currensees.com/v1/currencies/{uuid}?username={self.username}&day={self.day}&month={self.month}&year={self.year}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
