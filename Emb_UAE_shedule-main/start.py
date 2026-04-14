#58 sign in again
from main import *
import threading

chatIDs=[527234842,1,2]

'''try:
  t1 = threading.Thread(target=main, args=(chatIDs[1], 0, 39, 0, 59))
  t1.start()

except: 
  print(chatIDs[1], 'faild!!')

'''
#time.sleep(3
'''t1 = threading.Thread(target=main, args=(chatIDs[1], 0, 10, 0, 23))

t2 = threading.Thread(target=main, args=(chatIDs[0], 0, 20 , 0, 35))

t3 = threading.Thread(target=main, args=(chatIDs[2], 0, 8, 0, 23))

try:
  t3.start()
except: 
  print(chatIDs[2], 'faild!!')


try:
  t2.start()
except: 
  print(chatIDs[0], 'faild!!')


try:
  t1.start()
except: 
  
  print(chatIDs[1], 'faild!!')
'''