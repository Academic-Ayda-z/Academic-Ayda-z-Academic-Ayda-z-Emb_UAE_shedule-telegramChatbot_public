from urls import *
from keep_alive import *
import sys
import pickle
from selenium import webdriver
from chromedriver_py import binary_path
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

desired_date = [str(xdaysfromToday(10)), "2024-08-05"]
username='AydaZam'
password = "password"
email = 'email'
schedual_id = '57265065'
chat_id = 527234842
add_user(desired_date, chat_id, username,email, password)
'''with open('Users/allTeleBotUsersChatIdUser.pkl', "rb") as file2:
  chatBotUsers=pickle.load(file2)
'''
NUM_MONTHS_DURATION=6

allDrivers={}
#check paid
'''for id in chatBotUsers.keys():
    if chatBotUsers[id].paymentsNotifications[0]:
        all_users[id]=chatBotUsers[id]
        allDrivers[id]=getDriver()

user=all_users[527234842]
driver=allDrivers[527234842]'''
#print(user.location)


desired_date = [str(xdaysfromToday(8)), "2024-08-03"]
username='mahdi'
password = "@@password"
email = 'email'
schedual_id = ''
chat_id = 1

add_user(desired_date, chat_id, username,email, password)

chatID=1
user=all_users[chatID]
#user.schedual_id = schedual_id
 # this will get you the path variable
count_five_mins=0
flags=0
while True:
  if flags>=1:
    break
  #get driver
  driver=getDriver()
  while True:
    try:
      log_in(driver, user, sign_in_duabi)
      break
    except:
      print("login_refresh")
      driver.refresh()

  #click continue to get the shedual_id
  driver.find_element(By.XPATH,'//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
  time.sleep(sleep_time)
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
  
  while True:

    #logged in successfully and now chooseing place and date and time

    while True:
      if datetime.now().minute==57:
        flag=1
        flags+=1
        driver.quit()
        break 
      
      with open('openDates.txt','r') as f:
        lines=f.readlines()
      newDate=0

      for line in lines:
        
        AVdate=datetime.strptime(line.strip(), '%Y-%m-%d')
        print('newDate',AVdate)
        if AVdate<=datetime.strptime(user.desired_date[1], '%Y-%m-%d') and AVdate>=datetime.strptime(user.desired_date[0], '%Y-%m-%d'):
          newDate=1
          break
        else:
          newDate=0
          
      if newDate==0:
        time.sleep(5)

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
          time.sleep(5*60)
        
      print(count_select_duabi)

    if flag==1:
      time.sleep(180*3)
      with open('openDates.txt','w') as f:
            pass

      break

    with open('openDates.txt','w') as f:
            pass

  
    # Find the month and year
    '''  exSysOut = sys.stdout
      with open("test.out", 'w') as f:
        sys.stdout = f'''
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

    print(open_month_days_)

    with open('result.txt','w') as f:

      f.write(str(open_month_days_))

    '''for i in range(user.desired_num_months):
      go_to_prev_month_calender(driver)'''

    date = user.desired_date[0].split('-')
    year, month = date[0], date[1]
    go_to_start_of_desired_dates(driver, year, month)

    #attempt=0

    choose_day_time(driver, user)

    print('done')


    #if attemppt===0 {username}-{user_id}
    with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
      attempt = int(schedule_appointment.readline())
      if attempt == 0:
        with open('TODO/finished.txt','a') as f:
          print('findished')
          f.writelines(user.chatId)  



    driver.refresh()
    #driver.get(appointment_url)
    #sys.stdout = exSysOut
    for i in range(5*60):
      if datetime.now().minute==5 or datetime.now().minute==57:
        break
      if datetime.now().minute%5==0  and datetime.now().second>44 or (datetime.now().minute%5==1  and datetime.now().second<2):
        print(datetime.now())
        count_five_mins+=1
        break

      else:
        time.sleep(1)
    
    if datetime.now().minute==57:
      time.sleep(50)
      count_five_mins=0
      flag=1
      flags+=1
      with open('openDates.txt','w') as f:
            pass

      driver.quit()
      break
      
  