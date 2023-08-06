'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

import os
from modules import trade
from modules import send
from modules import wallet
from modules.utils.data import *

try:
    data = jsonBase("./data")
except FileNotFoundError:
    print("JSON file not found.")

commands = {
    "trade": trade.trade_function,
    "send": send.send_function,
    "wallet": wallet.wallet_function
}


def handle_command(user_input):
    try:
        command_list = user_input.split()
        command = command_list[0]
        args = command_list[1:]
    except:
        return {"status": "error", "error_code": "FIELD_EMPTY", "error_message": "Field is empty"}

    if command in commands:
        try:
            money_redeemed = data.load(args[0], "redeemed?") or False
            if not money_redeemed:
                usdBal = data.load(args[0], "usd")
                data.save(args[0], "usd", usdBal + 2000)
                data.save(args[0], "redeemed?", True)
            return commands[command](*args)
        except Exception as e:
            return {"status": "error", "error_code": "UNKNOWN_ERROR", "error_message": str(e)}
    else:
        return {"status": "error", "error_code": "INVALID_COMMAND", "error_message": "Invalid command"}


def main():
    while True:
        user_input = input("Enter a command: ")
        output = handle_command(user_input)
        print(output)


if __name__ == "__main__":
    main()
