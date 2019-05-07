"""
Module containing functions that fetch current cryptocurrency prices from exchanges.
Each function checks for active cryptocurrencies and requests the 
current price through the exchange's api
"""
import requests, json

#bitmex
def get_bitmex(pair):
    data = requests.get("https://www.bitmex.com/api/v1/instrument/active").json()
    coin_dict = {}
    for i in data:
        coin_dict[i['symbol']] = format(i['lastPrice'], 'f')
    try:
        return coin_dict[pair.upper()]
    except:
        return False

# binance
def get_binance(pair):
        pass