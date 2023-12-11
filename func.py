import requests
from telegram import *
from telegram.ext import *
from requests import *
from threading import Thread
from flask import Flask
import random

api_url = "https://randomuser.me/api/"
api = requests.get(api_url)
response = api.json()
username = response.get("results")[0]["login"]["username"]
pinfo = " ".join(response.get("results")[0]["name"].values())
user_matric_dict, matric_bid_dict = {},{}
choice = False

app = Flask('')

@app.route('/')

def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

def startCommand(update: Update, context: CallbackContext): #basic startup command
  buttons = [[KeyboardButton("/queue")],[KeyboardButton("/echo [message]")], 
             [KeyboardButton("/room")],[KeyboardButton("/check [room status]")],
             [KeyboardButton("/info")]]
  context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to RH room bidding!\
  Please enter your Matriculation Number using /matric [Matric Number].\n" + "Click the button at the side for\
  more commands! ", reply_markup=ReplyKeyboardMarkup(buttons))

def CheckTeleHandleHelper(update: Update, context: CallbackContext): #checks tele handle
  if update.message.chat.username not in user_matric_dict.keys():          
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your\
    Matriculation Number using /matric [Matric Number]")  
  else:
    return True

def UserInfoCommand(update: Update, context: CallbackContext): #gets user info
  if CheckTeleHandleHelper(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="@" + username
                             + "\n" + pinfo)

def EchoCommand(update: Update, context: CallbackContext) -> None: #echo message command
  context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text[6:])

def MatricNumberCommand(update: Update, context: CallbackContext):
  if update.message.text[8].upper() == 'A' and len(update.message.text[8:].strip(" ")) == 9 \
  and update.message.text.strip(" ")[-1].isalpha():
    if update.message.text.upper().strip(" ") not in user_matric_dict.values():
      user_matric_dict[update.message.chat.username] = update.message.text[8:].upper()
      context.bot.send_message(chat_id=update.effective_chat.id, text="Matriculation Number "
                               + update.message.text[8:].strip(" ") + " successfully registered!")
      print(user_matric_dict)
    elif update.message.text.upper().strip(" ") in user_matric_dict.values():
      context.bot.send_message(chat_id=update.effective_chat.id, text="Matriculation Number "
                               + update.message.text[8:].strip(" ") + " already registered!")
  else:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Invalid Matriculation Number, please try again")

def QueueStatusCommand(update: Update, context: CallbackContext): #outputs current + user queue no.
  if CheckTeleHandleHelper(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="@"
                             + update.message.chat.username + "\n" + "Current Number: "
                             + str(random.randint(1,69)) + "\n"
                             + "Your Number: " + str(random.randint(70,109)))

def RoomStatusCommand(update: Update, context: CallbackContext): #outputs room number bidded by user
  if CheckTeleHandleHelper(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your current bid: " + str(random.randint(2101,8820)))

def RoomAvailabilityCommand(update: Update, context: CallbackContext): #checks for room vacancy
  if CheckTeleHandleHelper(update, context):
    num = update.message.text[6:]
    ran = random.randint(0,1)
    if not num or len(num) != 4:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a valid room number.")
    elif ran and num:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Room number" + num
                               + " is available for bidding.")
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Room number" + num
                               + " is no longer available for bidding.")

def RoomBidCommand(update: Update, context: CallbackContext): #bids for room
  global choice, rm 
  if CheckTeleHandleHelper(update, context):
    rm = update.message.text.strip()[-1:-5:-1][::-1]
    if str(rm).isdigit() and \
    len(str(update.message.text).strip(" ")[5:]) == 4:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Would you like to bid for "
                               + rm + "? Type /confirm " + rm + " to confirm; /reject to cancel.")
      choice = True
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid room number.")
  
def confirmHelper(update: Update, context: CallbackContext): #confirms user bid
  global choice, rm
  cfm = update.message.text.strip()[-1:-5:-1][::-1]
  if choice and cfm == rm:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bid for room " + str(rm) + " confirmed.")
    choice = False
    matric_bid_dict[user_matric_dict[update.message.chat.username]] = rm
    rm = None
    print(matric_bid_dict)
  elif choice and cfm != rm:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Room mismatch, bid cancelled.")
    choice = False
    rm = None

def rejectHelper(update: Update, context: CallbackContext): #rejects user bid
  global choice, rm
  if choice:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bid cancelled.")
    choice = False
    rm = None

def endCommand(update: Update, context: CallbackContext): #outputs words you should hear
  context.bot.send_message(chat_id=update.effective_chat.id,
                           text="I am now useless, just like you.",
                           reply_markup = ReplyKeyboardRemove())
