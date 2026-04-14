import pickle

from mainExtention import *

def tehranTime():
  timeZ_Th = pytz.timezone('Asia/Tehran')
  now = datetime.now(timeZ_Th)
  return now

def dateNow():
  now = tehranTime()
  now = now.strftime( '%Y-%m-%d')
  return now

with open('Users/allTeleBotUsersChatIdUser.pkl', "rb") as file2:
    chatBotUsers=pickle.load(file2)

for u in chatBotUsers:
    print(chatBotUsers[u].desired_date, datetime.strftime( datetime.strptime( dateNow(),  '%Y-%m-%d') + timedelta(days=14) , "%Y-%m-%d"))
    diff=datetime.strptime( dateNow(),  '%Y-%m-%d').date()- datetime.strptime(chatBotUsers[u].desired_date[0], "%Y-%m-%d").date()

    '''if datetime.strftime( datetime.strptime( dateNow(),  '%Y-%m-%d') + timedelta(days=14) , "%Y-%m-%d") == datetime.strptime(chatBotUsers[u].desired_date[0], "%Y-%m-%d").date():
        print(datetime.strptime(chatBotUsers[u].desired_date[0], "%Y-%m-%d").date())


    '''  
    print(datetime.strftime( datetime.strptime( chatBotUsers[u].desired_date[0],  '%Y-%m-%d') - timedelta(days=14) , "%Y-%m-%d"))
    print(dateNow()==datetime.strftime( datetime.strptime( chatBotUsers[u].desired_date[0],  '%Y-%m-%d') - timedelta(days=14) , "%Y-%m-%d"))
    #if dateNow() >= datetime.strftime( datetime.strptime( chatBotUsers[u].desired_date[0],  '%Y-%m-%d') - timedelta(days=14) , "%Y-%m-%d"):
    startDate = datetime.strftime( datetime.strptime(dateNow() ,  '%Y-%m-%d') + timedelta(days=14) , "%Y-%m-%d")
    print(type(startDate))