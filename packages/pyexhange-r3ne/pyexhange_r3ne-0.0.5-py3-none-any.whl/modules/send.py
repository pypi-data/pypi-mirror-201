'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

from modules.utils.finhub import *
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
