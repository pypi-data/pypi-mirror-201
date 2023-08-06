'''
Copyright (c) 2023 R3ne.net
'''

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def coingecko_get_data(crypto_name):
    crypto_name = crypto_name.lower()
    try:
        current_price = cg.get_price(ids=crypto_name, vs_currencies='usd')[crypto_name]['usd']

        symbol = cg.get_coin_by_id(id=crypto_name)['symbol'].upper()

        return {"price": current_price, "symbol": symbol}
    except:
        return None