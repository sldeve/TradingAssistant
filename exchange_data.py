"""
Module containing functions that fetch current cryptocurrency prices.
Each function checks for active cryptocurrencies and requests the 
current price through the exchange's api
"""
import requests, json

#bitmex
def get_bitmex(coin):
    data = requests.get("https://www.bitmex.com/api/v1/instrument/active").json()
    for x in data:
        print(x['symbol'])
        print(format(x['lastPrice'], 'f'))
get_bitmex("whats ui")
