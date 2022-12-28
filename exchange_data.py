"""
Module containing functions that fetch current cryptocurrency, physical currency and stock
prices from exchanges. Each function takes the trading pair as a parameter and then checks 
the exchanges api for a matching ticker. If one is found, the last price is returned.
"""

import requests, json

# Pairs should be inputted without special characters. 
# Ex) BTCUSD not BTC/USD

# CRYPTOCURRENCIES

def get_bitmex(pair):
    data = requests.get("https://www.bitmex.com/api/v1/instrument/active").json()
    for i in data:
        if i['symbol']  == pair.upper():
            return float(i['lastPrice'])
    return False

def get_binance(pair):
    data = requests.get("https://api.binance.us/api/v1/ticker/24hr").content.decode("utf-8")
    data = json.loads(''.join(data))
    for i in data:
        if pair.upper() == i['symbol']:
            return float(i['lastPrice'])
    return False

def get_coinbase(pair):
    data = requests.get("https://api.pro.coinbase.com/products").json()
    for i in data:
        ticker = i['id']
        if ticker.replace("-","") == pair.upper():
            price = requests.get("https://api.pro.coinbase.com/products/"+ticker+"/ticker").json()
            return float(price['price'])
    return False

# FOREIGN EXCHANGE CURRENCIES

def get_forex(pair):
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency="+ pair[0:3] +"&to_currency="+ pair[3::] +"&apikey=INSERT TOKEN HERE"
    data = requests.get(url).json()
    return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])


# STOCK PRICES

def get_stock(symbol):
    try:
        url = "https://cloud.iexapis.com/stable/stock/market/batch?symbols=+"+symbol+"+&types=price&token=INSERT API KEY HERE"
        data = requests.get(url).json()
        return float(data[symbol]['price'])
    except:
        return False

def get_price(exchange, pair):
    if exchange.lower() == 'bitmex':
        return get_bitmex(pair)
    elif exchange.lower() == 'binance':
        return get_binance(pair)
    elif exchange.lower() == 'qtrade':
        return get_qtrade(pair)
    elif exchange.lower() == 'bittrex':
        return get_bittrex(pair)
    elif exchange.lower() == 'coinbase':
        return get_coinbase_pro(pair)
    elif exchange.lower() == "forex":
        return get_forex(pair.upper()) 
    elif exchange.lower() == 'stock':
        return get_stock(pair.upper())
    else:
        return False
