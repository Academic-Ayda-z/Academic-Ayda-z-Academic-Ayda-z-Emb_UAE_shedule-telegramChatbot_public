from init import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
import time
from chromedriver_py import binary_path
import urllib.request, json 
import requests

sleep_time = 5

STEP_TIME = 60*10

class_month = 'ui-datepicker-month'
class_year = 'ui-datepicker-year'
#duabi  abu dahbi is 49
FACILITY_ID=50

def getDriver():
  svc = webdriver.ChromeService(executable_path=binary_path)
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
  #chrome_options.add_argument('--headless=new')
  driver = webdriver.Chrome(options=chrome_options,service=svc)
  chrome_options.add_argument('--disable-dev-shm-usage')
  return driver

def set_user_schedule_id(user, schedual_id):
  global all_users
  user.schedual_id = schedual_id
  all_users[user.chatId].schedual_id = schedual_id


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


def month_diff(date1, date2):
  date1 = datetime.strptime(str(date1), '%Y-%m-%d')
  date2 = datetime.strptime(str(date2), '%Y-%m-%d')

  r = relativedelta.relativedelta(date2, date1)
  return r.months


def auto_action(driver, label, find_by, el_type, action, value):
  print("\t" + label + ":", end="")
  # Find Element By
  match find_by.lower():
    case 'id':
      item = driver.find_element(By.ID, el_type)
    case 'name':
      item = driver.find_element(By.NAME, el_type)
    case 'class':
      item = driver.find_element(By.CLASS_NAME, el_type)
    case 'xpath':
      item = driver.find_element(By.XPATH, el_type)
    case _:
      return 0
  # Do Action:
  match action.lower():
    case 'send':
      item.send_keys(value)
    case 'click':
      item.click()
    case _:
      return 0
  print("\t\tCheck!")


def SCHEDUAL_APPOINTMENT_SUBMIT(driver,user):
  with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'r+') as schedule_appointment:
    attempt = int(schedule_appointment.readline())

  if attempt == 0:
    print("already submitted. used all our attempts")
  elif attempt > 0:
    try:
 
      auto_action(driver, "", "name", "commit", "click", "")
      time.sleep(1)
      print("submitted")
      attempt -= 1
    except:
      print("could not submit!")
      pass
    
    html = driver.page_source
    with open("check_html_page.txt", 'a+') as page:
      page.write(f"{html}")
    with open("check_html.html", 'w') as page:
      page.write(f"{html}")

    with open(f"Users/{user.username}-{user.chatId}/schedule_count.txt", 'w') as schedule_appointment:
      schedule_appointment.write(f"{attempt}")
  else:
    print("num of attempts is negative! ERORR")

  try:
    #OK if there is
    auto_action(driver, "", "name", "commit", "click", "")
  except:
    print('OK was not needed')
    pass
def log_in(driver, user, url):
  # Open the URL in the WebDriver
  driver.get(url)
 
  '''with open('pageS.html','w+') as f:
    h = driver.page_source
    f.write(h)'''
  #sign in automatically
  Wait(driver,
       STEP_TIME).until(EC.presence_of_element_located((By.NAME, "commit")))
  #auto_action("Click bounce", "xpath", '//a[@class="down-arrow bounce"]', "click", "", STEP_TIME)
  auto_action(driver, "Email", "id", "user_email", "send", user.email)
  auto_action(driver, "Password", "id", "user_password", "send",
              user.password)
  auto_action(driver, "Privacy", "class", "icheckbox", "click", "")
  auto_action(driver, "", "name", "commit", "click", "")
  Wait(driver, STEP_TIME).until(
    EC.presence_of_element_located(
      (By.XPATH, "//a[contains(text(), '" + "Continue" + "')]")))


  print("\n\tlogin successful!\n")
  return True


def get_appointment_url(user, embassy):
  appointment_url = f"https://ais.usvisa-info.com/{embassy}/niv/schedule/{user.schedual_id}/appointment"
  return appointment_url


def select_duabi_Abu_dabi(driver, place):
  select = Select(
    WebDriverWait(driver, STEP_TIME).until(
      EC.element_to_be_clickable((
        By.XPATH,
        "//select[@class='required' and @name='appointments[consulate_appointment][facility_id]']"
      ))))
  select.select_by_visible_text(place)


def loadePageSelectPlace(driver,place):
  Wait(driver, 0).until(
  EC.presence_of_element_located(
  (By.XPATH, "//legend[contains(text(), '" + "Consular Section Appointment" + "')]")))
  #Abu Dhabi
  select_duabi_Abu_dabi(driver, place)

  Wait(driver, 60).until(
EC.presence_of_element_located(
(By.XPATH, '//*[@id="consulate_date_time"]/label[1]')))

  Wait(driver, 60).until(
          EC.presence_of_element_located(
            (By.XPATH,
            "//label[contains(text(), '" + "Date of Appointment" + "')]")))
  date_input = driver.find_element(
          By.NAME, "appointments[consulate_appointment][date]").click()
  
def current_year(driver):
  calendar_year = driver.find_element(By.CLASS_NAME, class_year).text
  return calendar_year


def current_month(driver):
  calender_month = driver.find_element(By.CLASS_NAME, class_month)
  current_calender_month = months_dict[calender_month.text]
  return current_calender_month


def update_table_trs(driver):
  table_class = 'ui-datepicker-calendar'
  table = driver.find_element(By.CLASS_NAME, table_class)
  tbody = table.find_element(By.TAG_NAME, "tbody")
  trs = tbody.find_elements(By.TAG_NAME, 'tr')  #5 trs
  return trs


def open_calender(driver):
  for i in range(5):
    try:
      Wait(driver, STEP_TIME).until(
        EC.presence_of_element_located(
          (By.XPATH,
           "//label[contains(text(), '" + "Date of Appointment" + "')]")))
      date_input = driver.find_element(
        By.NAME, "appointments[consulate_appointment][date]").click()
      break
    except:
      time.sleep(1)



def go_to_prev_month_calender(driver):
  Wait(driver, STEP_TIME).until(
    EC.presence_of_element_located(
      (By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div/a')))

  prev = driver.find_element(
    By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div/a').click()
  calender_month = driver.find_element(By.CLASS_NAME, class_month)
  current_calender_month = months_dict[calender_month.text]
  #print(f"Now we are in month {current_calender_month} aka {calender_month.text}",end='\n')
  return current_calender_month


def go_to_next_month_calender(driver):

  Wait(driver, STEP_TIME).until(
    EC.presence_of_element_located(
      (By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a')))

  next = driver.find_element(
    By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a').click()
  calender_month = driver.find_element(By.CLASS_NAME, class_month)
  current_calender_month = months_dict[calender_month.text]
  #print(    f"now we are in month {current_calender_month} aka {calender_month.text}",end='\n')
  return current_calender_month
