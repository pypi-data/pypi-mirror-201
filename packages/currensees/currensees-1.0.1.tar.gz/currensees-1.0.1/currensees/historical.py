import requests

class HistoricalRates:
    def __init__(self, username, date, day, month, year):
        self.username = username
        self.date = date
        self.day = day
        self.month = month
        self.year = year

    def get_historical_rates(self):
        url = f"https://currensees.com/v1/historical?username={self.username}&date={self.date}&day={self.day}&month={self.month}&year={self.year}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def get_historical_rate_by_uuid(self, uuid):
        url = f"https://currensees.com/v1/historical/{uuid}?username={self.username}&day={self.day}&month={self.month}&year={self.year}&date_string={self.date}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
