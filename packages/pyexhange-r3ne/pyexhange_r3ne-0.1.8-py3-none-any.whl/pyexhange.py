'''
Copyright (c) 2023 R3ne.net
'''

import os
import importlib
from modules.utils.data import *

try:
    data = jsonBase("./data")
except FileNotFoundError:
    print("JSON file not found.")

commands = {}

for filename in os.listdir(os.path.join(os.path.dirname(__file__), "modules")):
    if filename.endswith(".py"):
        module_name = filename[:-3] # remove .py extension
        module = importlib.import_module("modules." + module_name)
        if hasattr(module, module_name + "_function"):
            commands[module_name] = getattr(module, module_name + "_function")



def handle_command(user_input):
    try:
        command_list = user_input.split()
        command = command_list[0]
        args = command_list[1:]
    except:
        return {"status": "error", "error_code": "FIELD_EMPTY", "error": "Field is empty"}

    if command in commands:
        try:
            money_redeemed = data.load(args[0], "redeemed?") or False
            if not money_redeemed:
                usdBal = data.load(args[0], "usd")
                data.save(args[0], "usd", usdBal + 2000)
                data.save(args[0], "redeemed?", True)
            return commands[command](*args)
        except Exception as e:
            return {"status": "error", "error_code": "UNKNOWN_ERROR", "error": str(e)}
    else:
        return {"status": "error", "error_code": "INVALID_COMMAND", "error": "Invalid command"}


def main():
    while True:
        user_input = input("Enter a command: ")
        output = handle_command(user_input)
        print(output)


if __name__ == "__main__":
    main()
