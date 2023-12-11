from telegram import *
from telegram.ext import *
from requests import *
import os, func

updater = Updater(token=os.environ['TOKEN'])
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", func.startCommand))
dispatcher.add_handler(CommandHandler("killthebot", func.endCommand))
dispatcher.add_handler(CommandHandler("echo", func.EchoCommand))
dispatcher.add_handler(CommandHandler("queue", func.QueueStatusCommand))
dispatcher.add_handler(CommandHandler("check", func.RoomAvailabilityCommand))
dispatcher.add_handler(CommandHandler("room", func.RoomStatusCommand))
dispatcher.add_handler(CommandHandler("matric", func.MatricNumberCommand))
dispatcher.add_handler(CommandHandler("info", func.UserInfoCommand))
dispatcher.add_handler(CommandHandler("bid", func.RoomBidCommand))
dispatcher.add_handler(CommandHandler("confirm", func.confirmHelper))
dispatcher.add_handler(CommandHandler("reject", func.rejectHelper))

updater.start_polling()

