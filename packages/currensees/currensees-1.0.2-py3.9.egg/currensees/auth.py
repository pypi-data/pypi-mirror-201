import requests

class CurrenseesAuth:
    def __init__(self, username, password):
        self.base_url = 'https://currensees.com/v1'
        self.username = username
        self.password = password

    def login(self):
        url = f"{self.base_url}/login"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
