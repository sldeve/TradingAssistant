import logging
import telegram
from exchange_data import get_bitmex, get_binance, get_qtrade, get_price
from telegram.ext import CommandHandler
from telegram.ext import Updater
"""
The following Token belongs to a test bot created during the 
development of the main bot. This is not the token that belongs 
to the bot that will be used in production.
"""

updater = Updater(token="820246863:AAHtUNlQvP4TaXO8GOYZ4bMqcxJzjOADKk0", use_context=True)

j = updater.job_queue

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

instructions = ("This is the Cryptocurrency Price Alert Bot\n" +
"To set a price alert,use the setalert command and enter an exchange trading pair and price as follows:\n" + 
"/setalert binance,btcusd,20000")

# /help command
def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=instructions)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# /setalert command
def setalert(update, context):
    message_text = update.message.text[10::]
    is_valid_request(message_text, update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text="Your Price Alert Was Set Successfully.")

setalert_handler = CommandHandler('setalert', setalert)
dispatcher.add_handler(setalert_handler)

# checks if the alert request is valid
def is_valid_request(msg,chat_id):
    # remove whitespace and split the chosen exchange,trading pair and price into a list
    msg = msg.replace(" ","").split(",")
    cur_price = float(get_price(msg[0].lower(),msg[1].lower()))
    if cur_price != False:
        if cur_price < float(msg[2]):
            trigger = '>'
        elif cur_price > float(msg[2]):
            trigger = '<'
        f = open("alert_requests.txt", "a")
        f.write(','.join(msg)+","+str(chat_id)+","+trigger+'\n')
        f.close()

# checks if a set alert has been reached
def check_prices(context):
    f = open("alert_requests.txt", "r")
    lines = f.readlines()
    f.close()
    f = open("alert_requests.txt", "w")
    for line in lines:
        line = line.split(",")
        cur_price = float(get_price(line[0].lower(),line[1].lower())) 
        if line[4] == '>' and cur_price > float(line[2]) or line[4] == '<' and cur_price < float(line[2]):
            response = line[1].upper() + " has reached " + line[2] + " on " + line[0]
            context.bot.send_message(chat_id = int(line[3]), text = response )
        else:
            f.write(",".join(line))

job_check_prices = j.run_repeating(check_prices, interval= 5, first =0)     


updater.start_polling()