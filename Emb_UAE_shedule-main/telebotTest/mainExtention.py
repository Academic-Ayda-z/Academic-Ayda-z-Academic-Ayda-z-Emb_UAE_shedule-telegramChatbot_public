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
from datetime import datetime
import pickle
import pytz 
import asyncio

def readERC20():
  with open("ERC20_Teter.txt", 'r') as file:
    hashStr = file.read()
  return hashStr
  

def getHasStrTxt():
  hashStr = readERC20()
  text="آدرس واریز تتر مطابق زیر می باشد:\n" +"شبکه :ERC20\n" + hashStr
  return text

sendPhotoText= getHasStrTxt()
allInlinebuttons=[   
  "شرایط و قوانین را خوانده و موافقم .",
    'اضافه کردن/ویرایش ایمیل',
    'اضافه کردن/ ویرایش رمز عبور',
                  'بازگشت به منو اصلی'
                 ]
allButtonsInAfterStartMenue = [
    "شرایط و هزینه ها", 
    "پرداخت هزینه",
    'نمایش تقویم',
    "اطلاعات کاربری",
     "پیام به پشتیبانی"
]

def timeNow():
  timeZ_Th = pytz.timezone('Asia/Tehran') 
  now = datetime.now(timeZ_Th) 
  now=now.strftime("%m/%d/%Y, %H:%M:%S")
  return now
  
def adminChatID():
  adminChatId=527234842
  return adminChatId



class TelegaBotUser:
  def init_payment(self):
      #false not true
      self.paymentsNotifications[1]= [True,False,datetime.now()]


  def __init__(self, chat_id,username):
      self.chatId = chat_id
      self.username=username
      self.email = ''
      self.password=''
      # Serializing time stored in now 
      self.initTime=timeNow()
      #payed? notification? date
      self.paymentsNotifications=dict()
      self.init_payment()



def initialization():
  paths=['Users/allTeleBotUsersChatIdUser.pkl','Users/allusernamesChatId.pkl']
  result=[]

  for path in paths:

      if not os.path.exists(path):
          with open(path, 'wb') as file:
              pickle.dump(dict(), file)


      with open(path, "rb") as file2:
          result.append(pickle.load(file2))


  return result
  
allTeleBotUsersChatID,usernamesChatId=initialization()

def sendAdminMsg(msg,context):
  adminId=adminChatID()
  context.bot.send_message(chat_id= adminId,
       text= msg)

def readPrincipals():
  with open('pricesAndPrincipals.txt', 'r') as file:
    pricesAndPrincipals = file.read()
  return pricesAndPrincipals


def checkPath(username,chatId):
  path = f'Users/{username}-{chatId}'
  if not os.path.exists(path):
    os.mkdir(path)

def checkPayment(chatId):
  user=allTeleBotUsersChatID[chatId]
  
  weeks=len(user.paymentsNotifications.keys())
  #print(user.paymentsNotifications[weeks][0])
  return user.paymentsNotifications[weeks][0]
  

def insertMsgtoChatHelpTxt(chatId,msg):
  global allTeleBotUsersChatID
  username=allTeleBotUsersChatID[chatId].username
  with open(f'Users/{username}-{chatId}/help-chat.txt', 'a+') as file:
    #forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    #print(message.chat_id)
    file.write(msg)
    file.write('\n')

def insertToToDoList(chatId,msg):
  global allTeleBotUsersChatID
  username=allTeleBotUsersChatID[chatId].username
  with open('TODO/ToCheckHelpRequests.txt', 'a+') as file:
    file.write(f'{username}-{chatId} time: {datetime.now()} \n')
