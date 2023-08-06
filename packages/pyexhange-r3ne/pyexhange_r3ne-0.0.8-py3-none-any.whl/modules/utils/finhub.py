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

def get_crypto_price(crypto_symbol):
    crypto_symbol = crypto_symbol.upper()
    try:
        timestamp = int(time.time())
        candles = finnhub_client.crypto_candles(f"BINANCE:{crypto_symbol}USDT", 'D', timestamp - 86400, timestamp)
        current_price = candles['c'][-1]
        
        # Store the price in cache
        cache[crypto_symbol] = current_price
        
        return current_price
    except finnhub.exceptions.FinnhubAPIException as e:
        # If rate limited, return the cached price
        if e.http_status == 429:
            if crypto_symbol in cache:
                return cache[crypto_symbol]
            else:
                return None
        else:
            return None
