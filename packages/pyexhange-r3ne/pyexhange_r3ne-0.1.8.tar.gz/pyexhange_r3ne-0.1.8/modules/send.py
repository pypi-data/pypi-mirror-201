'''
Copyright (c) 2023 R3ne.net
'''

from modules.utils.data import *

data = jsonBase("./data")

def send_function(*args):
    # Check if number of arguments is correct
    if len(args) != 5:
        return {"status": "failed", "error_code": "INVALID_ARGUMENTS", "error": "Invalid arguments. Usage: send [user] [user_to] [amount] [currency] [message]"}

    user, userTo, amount, currency, message = args
    currency = currency.upper()
    amount = abs(float(amount))
    myBal = data.load(user, currency)
    if myBal >= amount:
        myBal -= amount
        toBal = data.load(userTo, currency)
        toBal += amount
        data.save(user, currency, myBal)
        data.save(userTo, currency, toBal)
        output = {
            "status": "success",
            "amount": amount,
            "userTo": userTo,
            "currency": currency,
            "message": message
        }
        return output
    else:
        return {"status": "failed", "error_code": "INSUFFICIENT_FUNDS", "error": "Insufficient funds."}
