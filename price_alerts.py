import logging
import telegram
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
    pass

updater.start_polling()