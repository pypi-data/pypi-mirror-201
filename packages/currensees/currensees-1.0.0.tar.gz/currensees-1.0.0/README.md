# Currency API Python Package

The package provides convenient access to the [Currency API](https://moatsystems.com/currency-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install currensees
## OR
easy_install currensees
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

Usage Example
-------------

```python
from currensees.auth import CurrenseesAuth
from currensees.convert import CurrenseesConvert
from currensees.convert_all import CurrenseesConvertAll
from currensees.currencies import CurrenseesCurrencies
from currensees.historical import CurrenseesHistorical

# Replace 'username' and 'password' with your actual credentials
username = 'username'
password = 'password'

# Authenticate and log in
auth_client = CurrenseesAuth(username, password)
response = auth_client.login()

# Use the base_url from the auth_client instance
base_url = auth_client.base_url

# Convert between two currencies
convert_client = CurrenseesConvert(base_url)
convert_response = convert_client.convert('2023_04_02', 'GBP', 'CAD', 500)
print("Convert response:", convert_response)

# Convert to all currencies
convert_all_client = CurrenseesConvertAll(base_url)
convert_all_response = convert_all_client.convert_all('GBP', 120, '2023_04_02')
print("Convert All response:", convert_all_response)

# Get all currencies
currencies_client = CurrenseesCurrencies(base_url)
currencies_response = currencies_client.get_currencies(username, '02', '04', '2023')
print("Currencies response:", currencies_response)

# Get currency by UUID
# Replace '<uuid>' with a valid UUID for a currency
uuid = '<uuid>'
currency_by_uuid_response = currencies_client.get_currency_by_uuid(uuid, username, '02', '04', '2023')
print("Currency by UUID response:", currency_by_uuid_response)

# Get historical data
historical_client = CurrenseesHistorical(base_url)
historical_response = historical_client.get_historical_data(username, '2023_04_02', '02', '04', '2023')
print("Historical response:", historical_response)

# Get historical data by UUID
# Replace '<uuid>' with a valid UUID for a currency
uuid = '<uuid>'
historical_data_by_uuid_response = historical_client.get_historical_data_by_uuid(uuid, username, '02', '04', '2023', '2023_04_02')
print("Historical data by UUID response:", historical_data_by_uuid_response)
```

## Setting up an Currency API Account

Subscribe here for a [user account](https://moatsystems.com/currency-api/).


## Using the Currency API

You can read the [API documentation](https://docs.currensees.com/) to understand what's possible with the Currency API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [BSD 3-Clause License](./LICENSE).


## Copyright

(c) 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
