import requests

class CurrenseesHistorical:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_historical_data(self, username, date, day, month, year):
        url = f"{self.base_url}/historical"
        headers = {'Accept': 'application/json'}
        params = {
            'username': username,
            'date': date,
            'day': day,
            'month': month,
            'year': year,
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_historical_data_by_uuid(self, uuid, username, day, month, year, date_string):
        url = f"{self.base_url}/historical/{uuid}"
        headers = {'Accept': 'application/json'}
        params = {
            'username': username,
            'day': day,
            'month': month,
            'year': year,
            'date_string': date_string,
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
