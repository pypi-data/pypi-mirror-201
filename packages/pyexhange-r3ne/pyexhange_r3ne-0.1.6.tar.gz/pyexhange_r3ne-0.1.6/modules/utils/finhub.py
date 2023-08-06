'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

import json
import os
import time
import finnhub

with open(os.path.join("./config.json")) as f:
    config = json.load(f)
    api_key = config["finhub_key"]
    finnhub_client = finnhub.Client(api_key=api_key)

# Dictionary to store cached prices
cache = {}

def finhub_get_data(crypto_symbol):
    crypto_symbol = crypto_symbol.upper()
    try:
        timestamp = int(time.time())
        candles = finnhub_client.crypto_candles(f"BINANCE:{crypto_symbol}USDT", 'D', timestamp - 86400, timestamp)
        current_price = candles['c'][-1]
        
        return {"price": current_price, "symbol": crypto_symbol}
    except:
        return None