import logging
import telegram
from exchange_data import get_bitmex, get_binance, get_qtrade, get_price
from telegram.ext import CommandHandler
from telegram.ext import Updater

updater = Updater(token="INSERT TOKEN HERE", use_context=True)

j = updater.job_queue

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

instructions = ("This is the Cryptocurrency Price Alert Bot\n" +
"To set a price alert,use the setalert command and enter an exchange, trading pair and price as follows:\n" + 
"/setalert binance,btcusdc,20000\n" + "To get the current price of a coin on a supported exchange use the getprice command:\n"+
"/getprice qtrade, nyzobtc ")

# /help command
def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=instructions)

# /getprice command bot can fetch the price on any supported exchange
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
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text="Your Price Alert Was NOT Set Successfully. Try Again.")

# checks if the alert request is valid
def is_valid_request(msg,chat_id):
    # remove whitespace and split the chosen exchange,trading pair and price into a list
    msg = msg.replace(" ","").split(",")
    cur_price = get_price(msg[0].lower(),msg[1].lower())
    # if request is valid, add to 'database'
    if cur_price != False:
        if cur_price < float(msg[2]):
            trigger = '>'
        elif cur_price > float(msg[2]):
            trigger = '<'
        else:
            return False
        f = open("alert_requests.txt", "a")
        f.write(','.join(msg)+","+str(chat_id)+","+trigger+'\n')
        f.close()
    else: 
        return False

# bot continuously checks if an alert has been reached
def check_prices(context):
    f = open("alert_requests.txt", "r")
    lines = f.readlines()
    f.close()
    f = open("alert_requests.txt", "w")
    for line in lines:
        line = line.split(",")
        cur_price = get_price(line[0].lower(),line[1].lower())
        if line[4][0] == '>'  and cur_price >= float(line[2]) or line[4][0] == '<' and cur_price <= float(line[2]):
            response = line[1].upper() + " has reached " + line[2] + " on " + line[0]
            context.bot.send_message(chat_id = int(line[3]), text = response )
        else:
            f.write(",".join(line))

if __name__ == "__main__":
    # bot checks prices with an interval of every 5 seconds    
    job_check_prices = j.run_repeating(check_prices, interval= 5, first =0)
    # create and add handlers to dispatcher
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)     
    setalert_handler = CommandHandler('setalert', setalert)
    dispatcher.add_handler(setalert_handler)
    getprice_handler = CommandHandler('getprice', getprice)
    dispatcher.add_handler(getprice_handler)
    updater.start_polling()
