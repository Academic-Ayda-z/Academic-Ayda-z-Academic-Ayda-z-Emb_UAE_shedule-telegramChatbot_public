
import sys
import pickle
from selenium import webdriver
from chromedriver_py import binary_path
import json, requests 
from urls import *
from datetime import datetime, timedelta
import pytz
from dateutil import relativedelta

def tehranTime():
  timeZ_Th = pytz.timezone('Asia/Tehran')
  now = datetime.now(timeZ_Th)
  return now


emb_Facilityid={'Dubai': 50 ,'Abu Dhabi': 49}

'''desired_date = [str(xdaysfromToday(5)), "2024-09-03"]
username='AydaZam'
password = ""
email = '@gmail.com'
schedual_id = '57265065'
chat_id = 527234842
add_user(desired_date, chat_id, username,email, password)
'''
'''with open('Users/allTeleBotUsersChatIdUser.pkl', "rb") as file2:
  chatBotUsers=pickle.load(file2)
'''


#check paid
'''for id in chatBotUsers.keys():
    if chatBotUsers[id].paymentsNotifications[0]:
        all_users[id]=chatBotUsers[id]
        allDrivers[id]=getDriver()

user=all_users[527234842]
driver=allDrivers[527234842]'''
#print(user.location)

def checkLogin(chatID):

  with open('Users/allTeleBotUsersChatIdUser.pkl', "rb") as file2:
    chatBotUsers=pickle.load(file2)

  user=chatBotUsers[chatID]
  #user.schedual_id = schedual_id
  # this will get you the path variable
  count_five_mins=0 
  flags=0
  flag=0

  driver=getDriver()

  try:
    log_in(driver, user, sign_in_duabi)
    return 1
  except:
    return 0
    