from telegram import *
from telegram.ext import *
from requests import *
import os

updater = Updater(token=os.environ['TOKEN'])
dispatcher = updater.dispatcher

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Tap to make money")], [KeyboardButton("Tap to do nothing")], [KeyboardButton("Tap to kick the bot")], [KeyboardButton("PAY 9371 3379")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))
def endCommand(update: Update, context: CallbackContext):
  
  context.bot.send_message(chat_id=update.effective_chat.id, text="I am now useless", reply_markup = ReplyKeyboardRemove())

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CommandHandler("killthebot", endCommand))

updater.start_polling()

