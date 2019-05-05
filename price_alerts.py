import logging
import telegram
from exchange_data import get_bitmex, get_binance
from telegram.ext import CommandHandler
from telegram.ext import Updater
"""
The following Token belongs to a test bot created during the 
development of the main bot. This is not the token that belongs 
to the bot being used in production.
"""

updater = Updater(token="820246863:AAHtUNlQvP4TaXO8GOYZ4bMqcxJzjOADKk0",use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# /help command
def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="This is the Cryptocurrency Price Alert Bot")

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# /setalert command
def setalert(update, context):
    message_text = update.message.text[10::]
    is_valid_request(message_text)


setalert_handler = CommandHandler('setalert', setalert)
dispatcher.add_handler(setalert_handler)

# checks if the alert request is valid
def is_valid_request(msg):
    # remove whitespace and split exchange, trading pair and price into a list
    msg = msg.replace(" ","")
    msg = msg.split(",")
    if msg[0].lower() == "bitmex" and get_bitmex(msg[2]) == True:
         store_request(msg)

# store_request in database
def store_request(data):
    pass

updater.start_polling()