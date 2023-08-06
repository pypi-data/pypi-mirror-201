'''
Copyright (c) 2023 R3ne.net
'''

from modules.utils.finhub import *
from modules.utils.coingecko import *

def get_data(crypto):
    #Maybe stonks too?!?!
    finhub_price = finhub_get_data(crypto)
    coingecko_price = coingecko_get_data(crypto)
    price = None

    if finhub_price == None:
        price = coingecko_price
    if coingecko_price == None:
        price = finhub_price
    return price