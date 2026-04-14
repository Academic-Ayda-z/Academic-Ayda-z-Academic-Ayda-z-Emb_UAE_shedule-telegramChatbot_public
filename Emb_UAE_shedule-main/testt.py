import calendar
from datetime import datetime
from dateutil import relativedelta
from datetime import date
import pytz
from datetime import datetime, timedelta

def check_date_format(date):
  try:
    date1 = datetime.strptime(str(date), '%Y-%m-%d')
    return True
  except:
    return False

def xdaysfromToday(Days=7):
  def tehranTime():
    timeZ_Th = pytz.timezone('Asia/Tehran')
    now = datetime.now(timeZ_Th)
    return now

  def dateNow():
    now = tehranTime()
    now = now.strftime("%m/%d/%Y")
    return now

  timeTemp = datetime.strftime( datetime.strptime( dateNow(), "%m/%d/%Y") + timedelta(days=Days) , "%Y-%m-%d")
  return timeTemp



def get_desired_num_months(dates):
  _dates = ['', '']
  _dates[0] = datetime.strptime(str(dates[0]), '%Y-%m-%d')
  _dates[1] = datetime.strptime(str(dates[1]), '%Y-%m-%d')

  r = relativedelta.relativedelta(_dates[1], _dates[0])
  if r.months >= 0:
    return r.months + 3
  print("the order of desired monts most be from the first to the last")
  return -1



all_users={}
def set_date(dates):
  today = datetime.today()
  # worng final just be less

  if check_date_format(dates[0]) == False:
    print("initiate date is not in the correct format")
    return []

  if check_date_format(dates[1]) == False:
    print("final date is not in the correct format")
    return []

  if get_desired_num_months(dates) > 15:
    print("the duration must be less than a year!")
    return []

  return dates


class User:

  def __init__(self, chat_id, desired_dates):
    self.chatId = chat_id
    self.username=''
    self.password = ""
    self.email = ""
    self.location = ""
    self.schedual_id = ""
    self.paymentsNotifications=[]
    self.desired_date =set_date(desired_dates)
    

def add_user(desired_date, chat_id, username, email_add, password):
  global all_users
  new_user = User(chat_id, desired_date)
  all_users[chat_id] = new_user
  all_users[chat_id].password = password
  all_users[chat_id].email = email_add
  all_users[chat_id] .username=username
  #get mrv and append to users mrv TODO

  #add schedual id
  return new_user



desired_date = [xdaysfromToday(4), "2024-07-22"]
username='AydaZam'
password = "password"
email = 'email'
schedual_id = '57265065'
chat_id = 527234842
add_user(desired_date, chat_id, username,email, password)

chatID= chat_id
user=all_users[chatID]

x=[{'date': '2024-08-01', 'business_day': True}, {'date': '2025-07-02', 'business_day': True}, {'date': '2025-07-03', 'business_day': True}, {'date': '2025-07-07', 'business_day': True}, {'date': '2025-07-08', 'business_day': True}, {'date': '2025-07-09', 'business_day': True}, {'date': '2025-07-10', 'business_day': True}]
def get_an_available_date(dates,user):
    # Evaluation of different available dates
    if dates==[]:
        return None
    def is_in_period(date, PSD, PED):
        new_date = datetime.strptime(date, "%Y-%m-%d")
        result = ( PED >= new_date and new_date >= PSD )
        # print(f'{new_date.date()} : {result}', end=", ")
        return result
    
    PED = datetime.strptime(user.desired_date[1], "%Y-%m-%d")
    PSD = datetime.strptime(user.desired_date[0], "%Y-%m-%d")
    for d in dates:
        date = d.get('date')
        if is_in_period(date, PSD, PED):
            return date
    print(f"\n No available dates between ({PSD.date()}) and ({PED.date()})!    {chatID}")


av=get_an_available_date(x,user)
with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
    attempt = int(schedule_appointment.readline())
print(attempt)

if av:
   print('2')