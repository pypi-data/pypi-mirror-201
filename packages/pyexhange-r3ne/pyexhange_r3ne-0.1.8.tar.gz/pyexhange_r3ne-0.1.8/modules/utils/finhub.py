'''
Copyright (c) 2023 R3ne.net
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