"""
Module containing functions that fetch current cryptocurrency prices from exchanges.
Each function checks for active cryptocurrencies and requests the 
current price through the exchange's api
"""

import requests, json

#bitmex
def get_bitmex(pair):
    data = requests.get("https://www.bitmex.com/api/v1/instrument/active").json()
    for i in data:
        if i['symbol']  == pair.upper(): 
            return format(i['lastPrice'], 'f')
    return False

# binance
def get_binance(pair):
    data = requests.get("https://api.binance.com/api/v1/ticker/24hr").content.decode("utf-8")
    data = json.loads(''.join(data))
    for i in data:
        if pair.upper() == i['symbol']:
            return i['lastPrice']
    return False

# qtrade
def get_qtrade(pair):
    data = requests.get("https://api.qtrade.io/v1/tickers").json()
    data =data['data']['markets']
    for i in data:
        if i['id_hr'].replace('_','') == pair.upper():
            return i['last']
    return False

def get_price(exchange, pair):
    if exchange == 'bitmex':
        get_bitmex(pair)
    elif exchange == 'binance':
        get_binance(pair)
    elif exchange == 'qtrade':
        get_qtrade(pair)
    return False
