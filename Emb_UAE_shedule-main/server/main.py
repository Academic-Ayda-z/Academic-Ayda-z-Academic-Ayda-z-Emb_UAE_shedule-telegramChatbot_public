from urls import *
from keep_alive import *
import sys
from selenium import webdriver
from chromedriver_py import binary_path
# Save the original stdout
'''original_stdout = sys.stdout

# Redirect stdout to a file
f = open('output.txt', 'w')
sys.stdout = f'''

keep_alive()

#date = 'year-month-day'
'''with open("somefile.txt", "a") as f:
  f.write("{}\n".format(output))
'''

desired_date = ["2024-06-15", "2024-08-01"]
password = "password"
email = 'email'
schedual_id = '57265065'
chat_id = 0

user = add_user(desired_date, chat_id, email, password)
user.schedual_id = schedual_id
 # this will get you the path variable
count_five_mins=0
while True:
  svc = webdriver.ChromeService(executable_path=binary_path)

  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(options=chrome_options,service=svc)
  #chrome_options.add_argument('--disable-dev-shm-usage')

  #storing IVR account number
  #//TODO
  '''with open("info.txt",'a') as info:
    flag=int(info.readline().split('=')[1])'''
  #flag = 3  # sleep for 15*4*3 3h
  '''while True:
    if log_in(driver, user, sign_in_duabi) == False and flag > 0:
      time.sleep(61)
      flag -= 1
      with open("info.txt",'w') as info:
        info.write(f"flag={flag}")
    elif flag <= 0:
      print("you are blocke!")
      time.sleep(15*60) #sleep for 15 mins
      with open("info.txt",'a') as info:
        flag=int(info.readline().split('=')[1])
      if flag<= -180:
        flag=3
      else:
        flag-=1
      with open("info.txt",'w') as info:
        info.write(f"flag={flag}")
    else:
      break'''
  while True:
    try:
      log_in(driver, user, sign_in_duabi)
      print("login")
      break
    except:
      #refresh
      #driver.get(driver.current_url)
      print("login_refresh")
      #time.sleep(31)
      driver.refresh()
      #time.sleep(31)


  #click continue to get the shedual_id
  '''driver.find_element(By.XPATH,'//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()
  time.sleep(sleep_time)'''
  #print(driver.current_url)
  '''appointment_url_driver=driver.current_url
  schedual_id=appointment_url_driver.split('/')[-2]
  set_user_schedule_id(user,schedual_id)'''

  logged_in_url_driver = driver.current_url
  print(logged_in_url_driver)

  appointment_url = get_appointment_url(user, embassy)
  print(appointment_url)
  driver.get(appointment_url)
  count_select_duabi=0
  while True:

    #logged in successfully and now chooseing place and date and time

    while True:
      print(count_select_duabi)
      try:
        Wait(driver, 1).until(
  EC.presence_of_element_located(
  (By.XPATH, "//legend[contains(text(), '" + "Consular Section Appointment" + "')]")))
        
        select_duabi_Abu_dabi(driver, 'Dubai')

        Wait(driver, 1).until(
EC.presence_of_element_located(
(By.XPATH, '//*[@id="consulate_date_time"]/label[1]')))

        Wait(driver, 1).until(
          EC.presence_of_element_located(
            (By.XPATH,
            "//label[contains(text(), '" + "Date of Appointment" + "')]")))
        date_input = driver.find_element(
          By.NAME, "appointments[consulate_appointment][date]").click()
        break

      except:

        count_select_duabi+=1
        if count_select_duabi>4:

          '''Wait(driver, 1).until(
      EC.presence_of_element_located(
        (By.XPATH, "//a[contains(text(), '" + "This page isn’t working" + "')]")))'''
          driver.refresh()
          #driver.get(appointm ent_url)
          time.sleep(2)
          count_select_duabi=0
  
      '''    while True:
            try:
              #clicking on Date of appointment
              Wait(driver, 1).until(
                EC.presence_of_element_located(
                  (By.XPATH,
                  "//label[contains(text(), '" + "Date of Appointment" + "')]")))
              date_input = driver.find_element(
                By.NAME, "appointments[consulate_appointment][date]").click()
              break
            except:
              time.sleep(1)
'''
    # Find the month and year
    '''  exSysOut = sys.stdout
      with open("test.out", 'w') as f:
        sys.stdout = f'''
    calender_month = driver.find_element(By.CLASS_NAME, class_month)
    current_calender_month = months_dict[calender_month.text]
    current_year_driver = current_year(driver)

    print(months_dict[calender_month.text], " = ", calender_month.text,
          f"year is {current_year_driver}")

    date = user.desired_dates[0].split('-')
    year, month = date[0], date[1]
    go_to_start_of_desired_dates(driver, year, month)

    current_year_driver = current_year(driver)
    current_calender_month = current_month(driver)

    open_month_days_ = see_available_dates_till_desired_month(
      driver, user.desired_num_months, current_calender_month)

    print(open_month_days_)

    for i in range(user.desired_num_months):
      go_to_prev_month_calender(driver)

    date = user.desired_dates[0].split('-')
    year, month = date[0], date[1]
    go_to_start_of_desired_dates(driver, year, month)

    #attempt=0

    choose_day_time(driver, user)

    print('done')

    #if attemppt===0
    with open("schedule_count.txt", 'r+') as schedule_appointment:
        attempt = int(schedule_appointment.readline())
    if attempt == 0:
          break

    with open("isRunning.txt", 'r+') as running:
      run_count = int(running.readline())
    run_count += 1
    with open("isRunning.txt", 'w') as running:
      running.write(f"{run_count}")

    with open("result.txt", 'w') as running:
      running.write(f"{open_month_days_}")

    #driver.get(logged_in_url_driver)
    #show_result()
    #if attempt ==0 send email
    #time.sleep(1)
    driver.refresh()
    #driver.get(appointment_url)
    #sys.stdout = exSysOut
    for i in range(5*60):
      if datetime.now().minute%5==0  and datetime.now().second>41 and datetime.now().second<59:
        time.sleep(1)
        print(datetime.now())
        count_five_mins+=1
        break
      else:
        time.sleep(1)
    
    if count_five_mins and datetime.now().minute%5!=0:
      count_five_mins=0
      driver.quit()
      break
      
  
 

