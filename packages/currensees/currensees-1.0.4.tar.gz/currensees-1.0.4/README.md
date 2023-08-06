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
from currensees.auth import *
from currensees.convert import *
from currensees.convert_all import *
from currensees.currencies import *
from currensees.historical import *

# Authenticate and log in
username = '<username>'
password = '<password>'
auth = CurrenseesAuth(username, password)
login_response = auth.login()

# Currency conversion
converter = CurrencyConverter("GBP", "CAD", "500", "2023_04_02")
print(converter.convert())

# Convert all available currencies
converter = ConvertAllCurrencies("GBP", 120, "2023_04_02")
print(converter.convert())

# Retrieve all available currencies
currencies = Currencies(username, '02', '04', '2023')
print(currencies.get_currencies())

# Retrieve a currency by uuid
currencies = Currencies(username, '02', '04', '2023')
print(currencies.get_currency_by_uuid('594bffc4-d095-11ed-9e30-acde48001122'))

# Retrieve currencies historical rates
historical_rates = HistoricalRates(username, '2023_04_02', '02', '04', '2023')
print(historical_rates.get_historical_rates())

# Retrieve currencies historical rates by uuid
historical_rates = HistoricalRates(username, '2023_04_02', '02', '04', '2023')
print(historical_rates.get_historical_rate_by_uuid('fe86014c-d162-11ed-a2dc-acde48001122'))
```

## Setting up Currency API Account

Subscribe here for a [user account](https://moatsystems.com/currency-api/).


## Using the Currency API

You can read the [API documentation](https://docs.currensees.com/) to understand what's possible with the Currency API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [BSD 3-Clause License](https://moatsystems.com/assets/license/BSD_3_Clause.txt).


## Copyright

(c) 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
