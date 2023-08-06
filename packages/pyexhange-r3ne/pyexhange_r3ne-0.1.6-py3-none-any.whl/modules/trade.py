'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

from modules.utils.exchanges import *
from modules.utils.data import *

data = jsonBase("./data")

def trade_function(*args):
    if len(args) != 3:
        return {"status": "failed", "error_code": "INVALID_ARGUMENTS", "error": "Invalid arguments. Usage: trade [user] [amount] [currency]"}
    
    user, amount, currency = args
    currency = currency.upper()
    symbol = get_data(currency)['symbol']
    try:
        if float(amount) < 0:
            # If amount is negative, we are selling, so check if user has enough of the currency
            walletBal = data.load(user, symbol)
            if walletBal < abs(float(amount)):
                return {"status": "failed", "error_code": "INSUFFICIENT_FUNDS", "error": f"Insufficient {currency} funds"}
        cost = get_data(currency)['price']
        usdBal = data.load(user, "USD")
        if cost == None:
            return {"status": "failed", "error_code": "NO_CURRENCY_FOUND", "error": f"{currency} could not be found from the database."}
        else:
            cost *= abs(float(amount))
    except TypeError:
        return {"status": "failed", "error_code": "INVALID_AMOUNT", "error": "Invalid input for amount"}

    if float(amount) > 0:
        # If amount is positive, we are buying
        if usdBal >= cost:
            usdBal -= cost
            walletBal = data.load(user, symbol)
            walletBal += float(amount)
            data.save(user, "USD", usdBal)
            data.save(user, symbol, walletBal, "CRYPTO")
            output = {
                "status": "success",
                "amount": amount,
                "currency": symbol,
                "cost": cost
            }
            return output
        else:
            output = {
                "status": "failed",
                "error_code": "INSUFFICIENT_FUNDS",
                "error": "Insufficient USD funds"
            }
            return output
    else:
        # If amount is negative, we are selling
        usdBal += cost
        walletBal -= abs(float(amount))
        data.save(user, "USD", usdBal)
        data.save(user, symbol, walletBal, "CRYPTO")
        output = {
            "status": "success",
            "amount": amount,
            "currency": symbol,
            "cost": cost
        }
        return output

