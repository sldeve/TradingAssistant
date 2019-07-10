import logging
import telegram
from exchange_data import *
from telegram.ext import CommandHandler
from telegram.ext import Updater
from dbhelper import DBHelper

updater = Updater(token="INSERT TOKEN HERE", use_context=True)

j = updater.job_queue

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


instructions = ("This is the Cryptocurrency Price Alert Bot\n To set a price alert,use the setalert command and enter an exchange, trading pair and price as follows:\n /setalert binance,btcusdc,20000\n To get the current price of a coin on a supported exchange use the getprice command:\n /getprice qtrade, nyzobtc ")

# /help command
def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=instructions)

# /getprice command, bot can fetch the price on any supported exchange
def getprice(update, context):
    message_text = update.message.text[10::]
    msg = message_text.replace(" ","").split(",")
    ans = get_price(msg[0], msg[1])
    if ans == False:
        context.bot.send_message(chat_id=update.message.chat_id, text="Invalid Trading Pair or Exchange")   
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="The current price of " + msg[1].upper() + " on " + msg[0] + " is " + "{:.8f}".format(float(ans)))

# /setalert command
def setalert(update, context):
    try:
        message_text = update.message.text[10::]
        if is_valid_request(message_text, update.message.chat_id) == False:
            context.bot.send_message(chat_id=update.message.chat_id, text="Your Price Alert Was Not Set Successfully. Choose a valid price then try again.")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Your Price Alert Was Set Successfully.")
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, text="Your Price Alert Was NOT Set Successfully. Try Again.")
        print(e)

# checks if the alert request is valid
def is_valid_request(msg,chat_id):
    db = DBHelper()
    db.setup()
    # remove whitespace and split the chosen exchange,trading pair and price into a list
    msg = msg.replace(" ","").split(",")
    cur_price = get_price(msg[0],msg[1])
    # if request is valid, add to database
    if cur_price != False:
        if cur_price < float(msg[2]):
            trigger = '>'
        elif cur_price > float(msg[2]):
            trigger = '<'
        else:
            return False
        row_id = len(db.get_table()) + 1
        db.add_alert((row_id, msg[0], msg[1], msg[2], chat_id, trigger))
    else: 
        return False

# bot continuously checks if an alert has been reached
def check_prices(context):
    db = DBHelper()
    db.setup()

    # Sample Row in Database: (ID, Exchange, Pair, Price, chat_id, trigger)
    table = db.get_table()
    for row in table:
        cur_price = get_price(row[1],row[2])
        if row[5] == '>' and cur_price >= float(row[3]) or row[5] == '<' and cur_price <= float(row[3]):
            if row[1] == "stock":
                response = row[2].upper() + " has reached " + row[3]
            else:
                response = row[2].upper() + " has reached " + row[3] + " on " + row[1]
            db.remove_alert(row[0])
            context.bot.send_message(chat_id = row[4], text = response )
        
if __name__ == "__main__":
    #initialize database
    db = DBHelper()
    db.setup()

    # bot checks prices with an interval of every 5 seconds    
    job_check_prices = j.run_repeating(check_prices, interval= 20, first =0)
    # create and add handlers to dispatcher
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)     
    setalert_handler = CommandHandler('setalert', setalert)
    dispatcher.add_handler(setalert_handler)
    getprice_handler = CommandHandler('getprice', getprice)
    dispatcher.add_handler(getprice_handler)
    updater.start_polling()

