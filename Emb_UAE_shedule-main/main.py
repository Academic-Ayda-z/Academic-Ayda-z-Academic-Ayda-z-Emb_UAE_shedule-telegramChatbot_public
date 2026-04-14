
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

def openDatesNewDate(lines,user):
  newDate=0
  availableDate=''
  try:
    
    for line in lines:
      AVdate=datetime.strptime(line.strip(), '%Y-%m-%d')
    
      if AVdate<=datetime.strptime(user.desired_date[1], '%Y-%m-%d') and AVdate>=datetime.strptime(user.desired_date[0], '%Y-%m-%d'):
        #print('newDate',AVdate)
        newDate=1
        availableDate=str(AVdate.date())
        
        break
    
      else:
        newDate=0
  except:
    pass
  return newDate,availableDate

# Save the original stdout
'''original_stdout = sys.stdout

# Redirect stdout to a file
f = open('output.txt', 'w')
sys.stdout = f'''

#keep_alive()

#date = 'year-month-day'
'''with open("somefile.txt", "a") as f:
  f.write("{}\n".format(output))
'''

emb_Facilityid={'Dubai': 50 ,'Abu Dhabi': 49}


def main(chatID, delay=0, secondS=13, minuteE=0, secondE=23, endT=56):
  #exec(open('a.py').read())

  '''  desired_date = [str(xdaysfromToday(5)), "2024-09-03"]
    username='AydaZam'
    password = "password"
    email = 'email'
    schedual_id = '57265065'
    chat_id = 527234842
    add_user(desired_date, chat_id, username,email, password)'''
  '''with open('Users/allTeleBotUsersChatIdUser.pkl', "rb") as file2:
    chatBotUsers=pickle.load(file2)
  '''
  NUM_MONTHS_DURATION=2

  allDrivers={}
  #check paid
  '''for id in chatBotUsers.keys():
      if chatBotUsers[id].paymentsNotifications[0]:
          all_users[id]=chatBotUsers[id]
          allDrivers[id]=getDriver()

  user=all_users[527234842]
  driver=allDrivers[527234842]'''
  #print(user.location)

  '''
    desired_date = [str(xdaysfromToday(4)), "2024-09-03"]
    username='mahdi'
    password = "@@password"
    email = 'email'
    schedual_id = ''
    chat_id = 6

    add_user(desired_date, chat_id, username,email, password)


    desired_date = [str(xdaysfromToday(4)), "2024-09-03"]
    username='MS'
    password = '@password'
    email = "email"
    schedual_id = ''
    chat_id = 2

    add_user(desired_date, chat_id, username,email, password)
  '''  
  
 
  user=all_users[chatID]


  if dateNow() >= datetime.strftime( datetime.strptime( user.desired_date[0],  '%Y-%m-%d') - timedelta(days=14) , "%Y-%m-%d"):
    startDate = datetime.strftime( datetime.strptime(dateNow() ,  '%Y-%m-%d') + timedelta(days=14) , "%Y-%m-%d")
    user.desired_date[0]=startDate

  #user.schedual_id = schedual_id
  # this will get you the path variable
  count_five_mins=0
  flags=0
  flag=0



  with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
    attempt = int(schedule_appointment.readline())

  if attempt==0:
    return 
#while True:
  time.sleep(delay)
  
  '''if flags>1:
    break'''
  #get driver
  
  driver=getDriver()
 
  while True:
    try:
      log_in(driver, user, sign_in_duabi)
      break
    except:
      print("login_refresh")
      time.sleep(2*60)
      driver.refresh()

  time.sleep(sleep_time)
  #click continue to get the shedual_id
  driver.find_element(By.XPATH,  "//a[contains(text(), '" + "Continue" + "')]").click()
                      #'//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
  
  print(driver.current_url)
  appointment_url_driver=driver.current_url
  schedual_id=appointment_url_driver.split('/')[-2]
  set_user_schedule_id(user,schedual_id)
  logged_in_url_driver = driver.current_url

  appointment_url = get_appointment_url(user, embassy)
  print(appointment_url)
  driver.get(appointment_url)
  count_select_duabi=0
  flag=0

  
  JS_SCRIPT = ("var req = new XMLHttpRequest();"
            f"req.open('GET', '%s', false);"
            "req.setRequestHeader('Accept', 'application/json, text/javascript, */*; q=0.01');"
            "req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');"
            f"req.setRequestHeader('Cookie', '_yatri_session=%s');"
            "req.send(null);"
            "return req.responseText;")


  #FACILITY_ID  Continue
  FACILITY_ID= emb_Facilityid[user.location]
  
  REGEX_CONTINUE='Continue'
  current_url=driver.current_url
  DATE_URL = f"{current_url}/days/{FACILITY_ID}.json?appointments[expedite]=false"
  TIME_URL = f"{current_url}/times/{FACILITY_ID}.json?date=%s&appointments[expedite]=false"
  APPOINTMENT_URL = f"{current_url}/appointment"

  def get_time(date):
    time_url = TIME_URL % date
    session = driver.get_cookie("_yatri_session")["value"]
    script = JS_SCRIPT % (str(time_url), session)
    content = driver.execute_script(script)
    data = json.loads(content)
    time = data.get("available_times")[-1]
    #print(f"Got time successfully! {date} {time}")
    try:
      with open('r.txt','a+') as f:
        f.write(f"Got time successfully! {date} {time}\n")
    except:
      pass
    return time

  def get_date():
    # Requesting to get the whole available dates
    session = driver.get_cookie("_yatri_session")["value"]
    script = JS_SCRIPT % (str(DATE_URL), session)
    content = driver.execute_script(script)
    return json.loads(content)
  
  
  def get_an_available_date(dates,user):
      # Evaluation of different available dates
      if dates==[]:
        return None
      def is_in_period(date, PSD, PED):
          new_date = datetime.strptime(date, "%Y-%m-%d").date()
          result = ( PED >= new_date and new_date >= PSD )
          # print(f'{new_date.date()} : {result}', end=", ")
          return result
      
      PED = datetime.strptime(user.desired_date[1], "%Y-%m-%d").date()
      PSD = datetime.strptime(user.desired_date[0], "%Y-%m-%d").date()
      for d in dates:
          date = d.get('date')
          if is_in_period(date, PSD, PED):
              return date
      print(f"\n No available dates between ({PSD.date()}) and ({PED.date()})!    {chatID}")
  
  def reschedule(date):
    with open('r.txt','a+') as f:
      f.write(date,  f'{APPOINTMENT_URL} :)\n')
    try:
      time = get_time(date)
      if driver.current_url!=APPOINTMENT_URL:
        driver.get(APPOINTMENT_URL)
      headers = {
          "User-Agent": driver.execute_script("return navigator.userAgent;"),
          "Referer": APPOINTMENT_URL,
          "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
      }
      data = {
          "utf8": driver.find_element(by=By.NAME, value='utf8').get_attribute('value'),
          "authenticity_token": driver.find_element(by=By.NAME, value='authenticity_token').get_attribute('value'),
          "confirmed_limit_message": driver.find_element(by=By.NAME, value='confirmed_limit_message').get_attribute('value'),
          "use_consulate_appointment_capacity": driver.find_element(by=By.NAME, value='use_consulate_appointment_capacity').get_attribute('value'),
          "appointments[consulate_appointment][facility_id]": FACILITY_ID,
          "appointments[consulate_appointment][date]": date,}
      
      r = requests.post(APPOINTMENT_URL, headers=headers, data=data)
      if (r.text.find('Successfully Scheduled') != -1):
          title = "SUCCESS"
          msg = f"Rescheduled Successfully! {date} {time}"

          with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'w+') as schedule_appointment:
            attempt =str(0)
            schedule_appointment.write(attempt)

      else:
          title = "FAIL"
          msg = f"Reschedule Failed!!! {date} {time}"
      
      with open('r.txt','a+') as f:
        f.write(title,'\n', msg,'\n')
      return [title, msg]
    except:
      with open('r.txt','a+') as f:
        f.write('pass\n')
      pass

  def reschedule_last(avDate):
    with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
      attempt = int(schedule_appointment.readline())
    
    with open('AllopenDates.txt','a+') as f:
      f.write(f'{attempt}  \n')
    
    if attempt==1:
      reschedule(avDate)
      with open('AllopenDates.txt','a+') as f:
        f.write(avDate)
        f.write(' reschedule \n')

  
  while True:
    if tehranTime().minute==endT:
        driver.quit()
        time.sleep(60)
        break


    with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
      attempt = int(schedule_appointment.readline())
 
    
    avDate=''

    count_load=0
    
    while True:
      with open('openDates.txt','r') as f:
        lines=f.readlines()
      newDate,availableDate=openDatesNewDate(lines,user)

      if tehranTime().minute==endT:
        break
      
      if newDate==1:
        avDate = availableDate
        if attempt==1:
          reschedule_last(avDate)
          break

      if newDate==1 or (tehranTime().minute%5==0 and (tehranTime().second >= secondS) and tehranTime().second <= secondE):
        try:
          dates_=get_date()
          avDate=get_an_available_date(dates_,user)
          count_load=0
          
          if avDate:
            
            with open('AllopenDates.txt','a+') as f:
              f.write(avDate)
              f.write('\n')

            with open('openDates.txt','w+') as f:
              f.write(avDate)
              f.write('\n')

            if attempt==1:
              reschedule_last(avDate)
            break

          else:
            with open('openDates.txt','w+') as f:
              pass

        except:
          count_load+=1
          driver.refresh()
        
          if count_load>7:
            time.sleep(60*4)
            count_load=0

      
      else:  
          time.sleep(5)
          

      # Print Available dates:
  

    if tehranTime().minute==endT:
      
      count_five_mins=0
      flag=1
      flags+=1


      driver.quit()
      return
      break
      





'''
    while True:

      #logged in successfully and now chooseing place and date and time

      while True:
        if tehranTime().minute==56:
          flag=1
          flags+=1
          time.sleep(60*1)
   

          driver.quit()
          break 
        
        print(get_date(),get_an_available_date(get_date()))
        with open('openDates.txt','r') as f:
          lines=f.readlines()
        newDate=0

        for line in lines:
          
          AVdate=datetime.strptime(line.strip(), '%Y-%m-%d')
          
          if AVdate<=datetime.strptime(user.desired_date[1], '%Y-%m-%d') and AVdate>=datetime.strptime(user.desired_date[0], '%Y-%m-%d'):
            print('newDate',AVdate)
            newDate=1
            time.sleep(2)
       
            break
          
          else:
            newDate=0
            
        if newDate==0:

          
          

          time.sleep(6)

        

        try:
          #place= user.embLoc
          
          loadePageSelectPlace(driver,'Dubai')
          count_select_duabi=0
          flag=0
          flags=0
          break
        except:
          count_select_duabi+=1
          
          
          driver.refresh()
          

          if count_select_duabi%10>6:
            time.sleep(4*60)
          
        print(count_select_duabi)

      if flag==1:
        time.sleep(60*1)
        break

      with open('openDates.txt','w') as f:
              pass

    
      # Find the month and year
    
      print(get_date(),get_an_available_date(get_date()))
      calender_month = driver.find_element(By.CLASS_NAME, class_month)
      current_calender_month = months_dict[calender_month.text]
      current_year_driver = current_year(driver)

      print(months_dict[calender_month.text], " = ", calender_month.text,
            f"year is {current_year_driver}")

      date = user.desired_date[0].split('-')
      year, month = date[0], date[1]
      go_to_start_of_desired_dates(driver, year, month)

    

      current_year_driver = current_year(driver)
      current_calender_month = current_month(driver)

      open_month_days_ = see_available_dates_till_desired_month(
        driver, NUM_MONTHS_DURATION, current_calender_month)

      

      
      #print(open_month_days_)
      
    
      with open('isRunning.txt','a+') as f:
              f.write(str(tehranTime())+f'  {chatID} \n')
              
      with open('result.txt','w') as f:

        f.write(str(open_month_days_))



      date = user.desired_date[0].split('-')
      year, month = date[0], date[1]
      go_to_start_of_desired_dates(driver, year, month)

      #attempt=0
      with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
        attempt = int(schedule_appointment.readline())
        #print(attempt,attempt==1)

      if attempt!=0:
        choose_day_time(driver, user)

     
      print(tehranTime())
      print(chatID,'done')

      


      #if attemppt===0 {username}-{user_id}
      with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
        attempt = int(schedule_appointment.readline())



      driver.refresh()
      #driver.get(appointment_url)
      #sys.stdout = exSysOut
      for i in range(5*60):
        with open('openDates.txt','r') as f:
          lines=f.readlines()
        newDate=0

        for line in lines:
          
          AVdate=datetime.strptime(line.strip(), '%Y-%m-%d')
          
          if AVdate<=datetime.strptime(user.desired_date[1], '%Y-%m-%d') and AVdate>=datetime.strptime(user.desired_date[0], '%Y-%m-%d'):
            newDate=1
            print('newDate',AVdate)
            break
          else:
            newDate=0
            
        if newDate==1:
          break
          

        if tehranTime().minute==5 or tehranTime().minute==56:
          break

        if tehranTime().minute%5==0 and tehranTime().second >= secondS and tehranTime().second <= secondE:
          print(tehranTime())
          count_five_mins+=1

         

          break

        else:
          time.sleep(1)
      
      if tehranTime().minute==56:
        time.sleep(60*1)
        count_five_mins=0
        flag=1
        flags+=1


        driver.quit()
        break
        '''
    
  

