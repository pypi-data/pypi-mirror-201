'''
Copyright (c) 2023 R3ne.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def coingecko_get_crypto_price(crypto_name):
    crypto_name = crypto_name.lower()
    try:
        current_price = cg.get_price(ids=crypto_name, vs_currencies='usd')[crypto_name]['usd']

        return current_price
    except:
        return None