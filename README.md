# TradingAssistant Bot
This bot allows users to set price alerts and fetch the current price of any cryptocurrency on the following exchanges:
* Binance
* BitMex
* Coinbase

This bot can additionally set price alerts and fetch the current price of the following:
* Foreign exchange traded currencies
* Securities found on NYSE and NASDAQ

Bot Username: @The_Trading_Assistant_bot  

Link: http://t.me/The_Trading_Assistant_bot  

Send the bot the following message to get started:
/help

#### In Development
* Alerts Based on Technical Indicators
* Alerts Based on Large Price Movements
* Sentiment Analysis

## Running your own implementation
First make sure you have the following requirements installed:
* Python 3
* requests module `pip3 install requests`
* python-telegram-bot beta version 12.0 https://python-telegram-bot.org

In order to run your own implementation, complete the following steps:
1. Create a new Telegram bot https://core.telegram.org/bots and save your bot token
2. Generate a new API Key at https://alphavantage.co
3. Fork this repository 
4. Change into the forked repository directory and open the bot.py file
5. In bot.py replace "INSERT TOKEN HERE" with your bot token
6. In exchange_data.py replace "INSERT TOKEN HERE" with your alphavantage API key
7. Run bot.py
8. Enjoy

### Displaying current open positions
The TradingAssistant now has the capability to fetch all of your current open positions from BitMex and displays them in a formatted message. Due to privacy and security concerns the only way to access this feature is to run your own implementation of the bot.

In order to enable the position command on your own implementation, complete the following steps:
1. Generate and securely store BitMex API Keys
2. Open the bitmex.py file then replace the api_id and api_secret variables with their respective values.
3. Open the bot.py file then replace the api_id and api_secret variables with their respective values.
4. Save changes
5. Run bot.py
6. Enjoy
