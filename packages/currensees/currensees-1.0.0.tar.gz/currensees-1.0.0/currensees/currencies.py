import requests

class CurrenseesCurrencies:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_currencies(self, username, day, month, year):
        url = f"{self.base_url}/currencies"
        headers = {'Accept': 'application/json'}
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year,
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_currency_by_uuid(self, uuid, username, day, month, year):
        url = f"{self.base_url}/currencies/{uuid}"
        headers = {'Accept': 'application/json'}
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year,
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
