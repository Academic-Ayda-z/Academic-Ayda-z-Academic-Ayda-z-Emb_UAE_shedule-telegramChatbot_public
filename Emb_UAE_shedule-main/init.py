import calendar
from datetime import datetime
from dateutil import relativedelta
from datetime import date
import pytz
from datetime import datetime, timedelta

months = list(calendar.month_name)
months_dict = {}
months_names = {}
open_month_days = {}
i = 0
for m in months:
  months_names[i] = m
  months_dict[m] = i
  #open_month_days[i] = {}  #trs  tds
  i += 1


def tehranTime():
  timeZ_Th = pytz.timezone('Asia/Tehran')
  now = datetime.now(timeZ_Th)
  return now

def dateNow():
  now = tehranTime()
  now = now.strftime( '%Y-%m-%d')
  return now

def xdaysfromToday(Days=14):


  timeTemp = datetime.strftime( datetime.strptime( dateNow(),  '%Y-%m-%d') + timedelta(days=Days) , "%Y-%m-%d")
  return timeTemp

def get_month_days():
  open_month_days = {}
  for i in range(1, 13):
    open_month_days[i] = {}  #trs  tds
  return open_month_days


all_users = {}


def check_date_format(date):
  try:
    date1 = datetime.strptime(str(date), '%Y-%m-%d')
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
    self.desired_date = set_date(desired_dates)
    self.desired_num_months = get_desired_num_months(self.desired_date)
