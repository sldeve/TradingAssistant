"""
Module containing functions that fetch current cryptocurrency prices from exchanges.
Each function checks for active cryptocurrencies and requests the 
current price through the exchange's api
"""

import requests, json

#bitmex
def get_bitmex(pair):
    data = requests.get("https://www.bitmex.com/api/v1/instrument/active").json()
    got_price = False
    for i in data:
        if i['symbol']  == pair.upper():
            got_price = True 
            return float(i['lastPrice'])
    if got_price == False:
        return False

# binance
def get_binance(pair):
    data = requests.get("https://api.binance.com/api/v1/ticker/24hr").content.decode("utf-8")
    data = json.loads(''.join(data))
    got_price = False
    for i in data:
        if pair.upper() == i['symbol']:
            got_price = True
            return float(i['lastPrice'])
    if got_price == False:
        return False

# bittrex
def get_bittrex(pair):
    data = requests.get("https://api.bittrex.com/api/v1.1/public/getmarketsummaries").json()
    data = data['result']
    got_price = False
    for i in data:
        if i['MarketName'].replace('-','') == pair.upper():
            got_price = True
            return float(i['Last'])
    if got_price == False:
        return False

# qtrade
def get_qtrade(pair):
    data = requests.get("https://api.qtrade.io/v1/tickers").json()
    data =data['data']['markets']
    got_price = False
    for i in data:
        if i['id_hr'].replace('_','') == pair.upper():
            got_price = True
            return float(i['last'])
    if got_price == False:
        return False

def get_price(exchange, pair):
    if exchange.lower() == 'bitmex':
        return get_bitmex(pair)
    elif exchange.lower() == 'binance':
        return get_binance(pair)
    elif exchange.lower() == 'qtrade':
        return get_qtrade(pair)
    else:
        return False

