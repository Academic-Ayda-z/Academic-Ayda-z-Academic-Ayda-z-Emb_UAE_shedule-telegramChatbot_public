#source myenvE/bin/activate
#pgrep chrome | xargs kill -9      timedatectl   crontab -e
#52 18 15 7 * cd /home/EMB_UAE_lates/Emb_UAE_shedule && /home/EMB_UAE_lates/Emb_UAE_shedule/myenv/bin/python /home/EMB_UAE_lates/Emb_UAE_shedule/start.py
#/home/EMB_UAE_lates/Emb_UAE_shedule/a.py
token = 'token'
#kmpMoEqhVmUsUfPuYOEeWZinImbRQPzU/lym3OsFUjg= pub server
#WMDKlQbN1+gejExcbexvivpqfEpFlIY8sX/aJjOzJVk=  peer
#pip install -U aiogram
from telegram.ext import *
from telegram import *
import logging
import time

from requests import *
import os
from datetime import datetime, timedelta
import time
import pytz
from dateutil import relativedelta
import calendar
import asyncio

def tehranTime():
  timeZ_Th = pytz.timezone('Asia/Tehran')
  now = datetime.now(timeZ_Th)
  return now


updater = Updater(token=token)
dispatcher = updater.dispatcher

def showMenue(update: Update, context: CallbackContext):
    global allButtonsInAfterStartMenue

    addTeleBotUser(update.effective_chat.id, update.effective_chat.username)

    #print(update.effective_chat.username)
    #print(update.message.text)
    with open('isRunning.txt','r') as f:
        txt=f.read()
    
    text = txt,
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


dispatcher.add_handler(CommandHandler("start", showMenue))