'''
Copyright (c) 2023 R3ne.net
'''

from modules.utils.data import *
from modules.utils.exchanges import *

data = jsonBase("./data")

def wallet_function(*args):
    if len(args) != 2:
        return {"status": "failed", "error_code": "INVALID_ARGUMENTS", "error": "Invalid arguments. Usage: wallet [user] [currency]"}

    user, currency = args
    currency = currency.upper()
    curdata = get_data(currency)

    if curdata == None:
        curdata = {"price": 0, "symbol":"CRYPTO"}
    amount = data.load(user, curdata['symbol'])

    output = {"status": "success", "amount": amount,"price": curdata['price'] * amount, "currency": curdata['symbol']}
    return output
