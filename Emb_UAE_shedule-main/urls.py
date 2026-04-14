from simple_funcs import *
#get it from bot
embassy = "en-ae"
sign_in_duabi = f"https://ais.usvisa-info.com/{embassy}/niv/users/sign_in"


def go_to_start_of_desired_month(driver, desired_m, current_calender_m):
  while desired_m > current_calender_m:
    current_calender_m = go_to_next_month_calender(driver)

  while desired_m < current_calender_m:
    current_calender_m = go_to_prev_month_calender(driver)


def go_to_start_of_desired_dates(driver, desired_year, desired_month):
  current_calender_m = current_month(driver)
  year_we_are_now = current_year(driver)

  if year_we_are_now == desired_year:
    print("desired month is ", int(desired_month),
          f" current month is {current_calender_m}-{year_we_are_now}")
    go_to_start_of_desired_month(driver, int(desired_month),
                                 current_calender_m)

  elif int(year_we_are_now) > int(desired_year):
    print("Desired month is ", int(desired_month),
          f" current month is {current_calender_m}-{year_we_are_now}")

    lastM=current_calender_m
    while 12 > current_calender_m:
      current_calender_m = go_to_prev_month_calender(driver)
      if lastM==current_calender_m:
        break
      lastM=current_calender_m
    go_to_prev_month_calender(driver)
    go_to_start_of_desired_dates(driver, desired_year, desired_month)

  else:
    print(
      f"error current year is {year_we_are_now} and desired year is {desired_year}"
    )


def finding_the_soones_available_dates(driver, tr_index,
                                       current_calender_month):
  result_days = []
  trs = update_table_trs(driver)
  #print(tr_index)
  num_open_days = len(trs[tr_index].find_elements(By.TAG_NAME, "a"))
  if num_open_days == 0:
    #print(f'  No open Dates available in {months_names[current_calender_month]} week {tr_index}')
    return 0
  else:
    print(
      f'open days in {months_names[current_calender_month]} week {tr_index} are {num_open_days}:',
      end='\n')
    for i in range(num_open_days):
      print(trs[tr_index].find_elements(By.TAG_NAME, "a")[i].text)
      result_days.append(
        int(trs[tr_index].find_elements(By.TAG_NAME, "a")[i].text))
     
  return result_days


def see_available_dates_till_desired_month(driver, num_of_months,
                                           current_calender_month):
  global open_month_days
  open_month_days = {}
  calender_year = int(current_year(driver))
  open_month_days[calender_year] = get_month_days()
  open_month_days[calender_year + 1] = get_month_days()

  #print(num_of_months)
  while num_of_months > 0:
    calender_year = int(current_year(driver))
    for tr_index in range(5):
      availability = finding_the_soones_available_dates(
        driver, tr_index, current_calender_month)
      if availability != 0:

        with open('openDates.txt','a') as f:
          for day in availability:
            f.write(f'{calender_year}-{current_calender_month}-{day}\n')

        try:
          open_month_days[calender_year][current_calender_month][
            tr_index + 1].append(availability)
         

        except:
          open_month_days[calender_year][current_calender_month][tr_index +
                                                                 1] = []
          open_month_days[calender_year][current_calender_month][
            tr_index + 1].append(availability)
          
    current_calender_month = go_to_next_month_calender(driver)
    num_of_months -= 1

  return open_month_days


def choosing_day(driver, chosen_year, chosen_month, row, day, user):
  '''  current_calender_month = current_month(driver)
    go_to_prev_month_calender(driver)
    go_to_start_of_desired_dates(driver, user)'''
  #current_calender_month = current_month(driver)
  go_to_start_of_desired_dates(driver, chosen_year, chosen_month)
  start = 0
  for i in range(1, 8):
    start_td = driver.find_element(
      By.XPATH,
      f'//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[1]/td[{str(i)}]')
    if start_td.text == '1':
      start = i
      break

  column = day - 7 * (row - 1) + start - 1
  #day_xpath='//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[5]/td[3]'
  try:
    day_xpath = f'//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[{str(row)}]/td[{str(column)}]'
    driver.find_element(By.XPATH, day_xpath).click()
    print(
      f"day {day}, month {chosen_month}, year {current_year(driver)} was selected. now choose a time."
    )
    return True
  except:
    print("could not choose a day.")
    return False


def choosing_a_time(driver):

  options = driver.find_elements(By.TAG_NAME, "option")
  length_of_options = len(options)
  print(length_of_options)
  '''for x in range(length_of_options):
    try:
      time_text = driver.find_element(
        By.XPATH,
        f'//*[@id="appointments_consulate_appointment_time"]/option[{x}]').text
      print(time_text)
      select = Select(
        WebDriverWait(driver, STEP_TIME).until(
          EC.element_to_be_clickable((
            By.XPATH,
            "//select[@class='required' and @name='appointments[consulate_appointment][time]']"
          ))))
      print(f'x: {x}')
      break
    except:
      time.sleep(1)
'''

  for i in range(7,-1,-1):
 
    try:
      time_text = driver.find_element(
        By.XPATH,
        f'//*[@id="appointments_consulate_appointment_time"]/option[{i}]').text
      print(time_text," i: ",i)
      select = Select(
        WebDriverWait(driver, STEP_TIME).until(
          EC.element_to_be_clickable((
            By.XPATH,
            "//select[@class='required' and @name='appointments[consulate_appointment][time]']"
          ))))

      if(len(time_text)==len('07:15')):
        select.select_by_visible_text(time_text)
        print(time_text," time was selected.")
        return True

    except:
      print("time could not be selected :((()))")
      time.sleep(1)
  return False


# choose day..............and time.........
def choose_day_time(driver, user):
  global open_month_days

  desired_dates = user.desired_date
  start_date = desired_dates[0].split('-')
  end_date = desired_dates[1].split('-')
  start_day = int(start_date[2])
  start_month = int(start_date[1])
  start_year = int(start_date[0])
  success = 0
  year_flag = 0

  for chosen_month in range(start_month,
                            start_month + user.desired_num_months):

    chosen_month = chosen_month % 13
    if chosen_month == 0:
      chosen_month = 1

    if chosen_month == 12:
      year_flag = 1

    if open_month_days[start_year][chosen_month] != None:
      for row in open_month_days[start_year][chosen_month]:
        for days in open_month_days[start_year][chosen_month][row]:
          for day in days:
            current_date = datetime.strptime(
              f"{start_year}-{chosen_month}-{day}", '%Y-%m-%d')
            print(current_date)
            
            desired_begining_date = datetime.strptime(desired_dates[0],
                                                      '%Y-%m-%d')
            
            desired_ending_date = datetime.strptime(desired_dates[1],
                                                    '%Y-%m-%d')
            if desired_begining_date <= current_date and current_date <= desired_ending_date:
              if choosing_day(driver, str(start_year), chosen_month, row, day,
                              user) == True:
                print("success1")
                #time.sleep(3)
                if choosing_a_time(driver) == True:
                  with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt",
                            'r+') as schedule_appointment:
                    attempt = int(schedule_appointment.readline())
                  print(f'attempt : {attempt}')
                  if attempt > 0:
                    #time.sleep(30)
                    SCHEDUAL_APPOINTMENT_SUBMIT(driver,user)
                    
                    print('success2')
                  
                    success = 1
                    return True
                #click on shedual and appointment

              open_calender(driver)
              #time.sleep(sleep_time)

      if year_flag == 1:
        year_flag = 0
        start_year += 1

  return False
