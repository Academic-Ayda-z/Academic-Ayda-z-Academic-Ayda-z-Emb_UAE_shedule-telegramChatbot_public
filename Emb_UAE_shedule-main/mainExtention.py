token = 'token'
disableGuessImports = True
#pip install -U aiogram
from telegram import *
import logging
import time
from telegram.ext import *
from requests import *
from PIL import Image
import os
import asyncio
from datetime import datetime, timedelta
import time
import pickle
import pytz
from dateutil import relativedelta
import calendar
import asyncio


def readBEP():
  with open("BEP20_Teter.txt", 'r') as file:
    hashStr = file.read()
  return hashStr


def getHasStrTxt():
  hashStr = readBEP()
  text = "آدرس واریز تتر مطابق زیر می باشد:\n" + "شبکه :BEP20\n" + hashStr
  return text


sendPhotoText = getHasStrTxt()
allInlinebuttons = [
    "شرایط و قوانین را خوانده و موافقم .", 'اضافه کردن/ویرایش ایمیل',
    'اضافه کردن/ ویرایش رمز عبور', 'انتخاب سفارت', 'انتخاب بازه زمانی دلخواه',
    'تست ورود به حساب کاربری', 'بازگشت به منو اصلی'
]
allButtonsInAfterStartMenue = [
    "شرایط و هزینه ها", "پرداخت هزینه", "اطلاعات کاربری", "پیام به پشتیبانی"
]

EMBInlineButtons = ['دبی', 'بازگشت به منو اصلی']
embLoc = {EMBInlineButtons[0]: 'en-ae', 'en-ae': EMBInlineButtons[0]}

paymentButtons = ["validate", "cancel"]


def check_date_format(date):
  try:
    datetime.strptime(str(date), '%Y-%m-%d')
    return True
  except:
    return False


def get_desired_num_months(dates):
  _dates = ['', '']
  _dates[0] = datetime.strptime(str(dates[0]), '%Y-%m-%d')
  _dates[1] = datetime.strptime(str(dates[1]), '%Y-%m-%d')

  r = relativedelta.relativedelta(_dates[1], _dates[0])
  if r.months >= 0:
    return r.months + 3
  print("the order of desired monts most be from the first to the last")
  return -1


def tehranTime():
  timeZ_Th = pytz.timezone('Asia/Tehran')
  now = datetime.now(timeZ_Th)
  return now


def timeNow():
  now = tehranTime()
  now = now.strftime("%m/%d/%Y, %H:%M:%S")
  return now


def adminChatID():
  adminChatId = 7048890923
  return adminChatId


class TelegaBotUser:

  #valid number of payments so far when was the last payment

  def __init__(self, chat_id, username):
    self.chatId = chat_id
    self.username = username
    self.email = ''
    self.password = ''
    self.desired_date = ['', '']
    self.desired_num_months = 0
    self.schedual_id = ''
    self.location = ''
    # Serializing time stored in now
    self.initTime = timeNow()
    #payed? notification? date
    self.paymentsNotifications = [False, '0', timeNow()]


def initialization():
  if not os.path.exists('Users'):
    os.mkdir('Users')

  if not os.path.exists('TODO'):
    os.mkdir('TODO')
  paths = [
      'Users/allTeleBotUsersChatIdUser.pkl', 'Users/allusernamesChatId.pkl'
  ]
  result = []

  for path in paths:

    if not os.path.exists(path):
      with open(path, 'wb') as file:
        pickle.dump(dict(), file)

    with open(path, "rb") as file2:
      result.append(pickle.load(file2))

  return result


allTeleBotUsersChatID, usernamesChatId = initialization()


def updatePaymentStatus():
  global allTeleBotUsersChatID
  for user in allTeleBotUsersChatID.values():
    initDate = user.paymentsNotifications[2]

    if datetime.strptime(timeNow(), "%m/%d/%Y, %H:%M:%S") > datetime.strptime(
        initDate, "%m/%d/%Y, %H:%M:%S") + timedelta(days=7):
      user.paymentsNotifications[0] = False
      #send user noftification of expiration
      context.bot.send_message(
          chat_id=adminChatID(),
          text=
          'مدت زمان یک هفته ای شما برای پیدا کردن وقت سفارت به اتمام رسیده است. لطفا جهت تمدید عکس فیش پرداختی را ارسال نماید.'
      )


def updateInfo():
  global allTeleBotUsersChatID, usernamesChatId
  paths = [
      'Users/allTeleBotUsersChatIdUser.pkl', 'Users/allusernamesChatId.pkl'
  ]
  dicts = [allTeleBotUsersChatID, usernamesChatId]

  for i, path in enumerate(paths):
    with open(path, 'wb') as file:
      pickle.dump(dicts[i], file)


def forward_to_chat(update, context, message=''):
  text = f'{message}\n{update.message.from_user.id}\n {update.effective_chat.username}--{update.effective_chat.id}'

  forwarded = update.message.forward(chat_id=adminChatID())
  if not forwarded.forward_from:

    context.bot.send_message(chat_id=adminChatID(),
                             reply_to_message_id=forwarded.message_id,
                             text=text)


def sendAdminMsg(msg, context):
  adminId = adminChatID()
  context.bot.send_message(chat_id=adminId, text=msg)


def sendAdminPaymentScreenShot(context, path, caption):
  adminId = adminChatID()
  context.bot.send_photo(chat_id=adminId,
                         photo=open(path, 'rb'),
                         caption=caption)


def readPrincipals():
  with open('pricesAndPrincipals.txt', 'r') as file:
    pricesAndPrincipals = file.read()
  return pricesAndPrincipals


def checkFileOs(path):
  if not os.path.exists(path):
    os.mkdir(path)


def checkPath(username, chatId):
  path = f'Users/{username}-{chatId}'
  if not os.path.exists(path):
    os.mkdir(path)


def setLastPaymentStatus(chatId, value):

  user = allTeleBotUsersChatID[chatId]

  if value:
    user.paymentsNotifications[1] = str(int(user.paymentsNotifications[1]) + 1)

  if value == True and user.paymentsNotifications[0] == False:
    user.paymentsNotifications[0] = True
    user.paymentsNotifications[2] = timeNow()

  #user is paying sooner than it should so I assume they have payed the exact date that the deal expires
  elif value == True and user.paymentsNotifications[0] == True:
    user.paymentsNotifications[0] = True

    timeTemp = datetime.strptime(user.paymentsNotifications[2],
                                 "%m/%d/%Y, %H:%M:%S") + timedelta(days=7)
    user.paymentsNotifications[2] = timeTemp.strftime("%m/%d/%Y, %H:%M:%S")

  if value == False:
    user.paymentsNotifications[0] = False

  updateInfo()


def checkPayment(chatId):
  global allTeleBotUsersChatID
  user = allTeleBotUsersChatID[chatId]
  lastPayment = user.paymentsNotifications[0]
  return lastPayment


def insertMsgtoChatHelpTxt(chatId, msg):
  global allTeleBotUsersChatID
  username = allTeleBotUsersChatID[chatId].username
  with open(f'Users/{username}-{chatId}/help-chat.txt', 'a+') as file:
    #forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    #print(message.chat_id)
    file.write(f'{msg} \n')


def insertToToDoList(chatId, msg):
  global allTeleBotUsersChatID
  username = allTeleBotUsersChatID[chatId].username
  with open('TODO/ToCheckHelpRequests.txt', 'a+') as file:
    file.write(f'{username}-{chatId} time: {datetime.now()} \n')
