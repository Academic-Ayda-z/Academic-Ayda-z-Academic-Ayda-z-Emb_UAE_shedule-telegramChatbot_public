'''from datetime import datetime
hour= 23
while True:
    if datetime.now().hour==23:
        hour=datetime.now().hour
        exec(open('main.py').read())
        
    elif datetime.now().hour!= hour and hour!=23:
        hour=datetime.now().hour
        exec(open('main.py').read())

'''