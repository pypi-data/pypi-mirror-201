'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

from modules.utils.data import *
from modules.utils.exchanges import *


def price_function(*args):
    if len(args) != 2:
        return {"status": "failed", "error_code": "INVALID_ARGUMENTS", "error": "Invalid arguments. Usage: price system [currency]"}
    user, currency = args
    currency = currency.upper()

    try:
        return {
            "status": "success",
            "price": get_price(currency),
            "currency": currency,
        }
    except:
        return {"status": "failed", "error_code": "NO_CURRENCY_FOUND", "error": f"{currency} could not be found from the database."}
