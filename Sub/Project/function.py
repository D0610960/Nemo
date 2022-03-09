# In[1]:


import sensor_HC_SR04 as sensor
import motor_L298N as motor
import serial
import math
import time
import random
import numpy as np
import os
import pyrebase

# firebase basic
config = {
    "apiKey": "AIzaSyCZIO4jkPAZXIM_L1rEcu1LMx8JAFbe8-c",
    "authDomain": "nemo-site.firebaseapp.com",
    "databaseURL": "https://littlepi-78630.firebaseio.com",
    "projectId": "littlepi-78630",
    "storageBucket": "littlepi-78630.appspot.com",
    "messagingSenderId": "95913815433",
    "appId": "1:95913815433:web:3b8dcc3f9ad8bd831e0558",
    "measurementId": "G-4284WKWVBT"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()

# arduino variables
ser = serial.Serial('/dev/ttyUSB0', 9600)
direction = ['w', 'a', 's', 'd', 'q', 'e', 'x']
persent = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
speed = [0, 30, 40, 48, 56, 64, 72, 80, 90, 100]
humidity = 0
temperature = 0
gasValue = 0.0

# walking mode variables
dangerDis = 40
warningDis = 60
longTime = 0.5
shortTime = 0.33
disList_R = []
disList_L = []


# In[2]:


def static():
    motor.move('stop')


# read data from arduino Uno
def arduinoData():
    ans = []
    while True:
        s = ser.readline()
        if s != '':
            temp = str(s[0:-2])[2:-1]
        else:
            return 'n', ''
        
        if temp in direction:
            return 'd', temp
        elif temp in persent:
            return 's', temp
        else:
            ans.append(temp)
            if len(ans) == 3:
                return 'v', ans
            else:
                pass


def control():
    motor.changePWM(56)
    
    while True:
        try:
            mode, data = arduinoData()
            print(mode)
        except:
            mode, data = 'n', ''
            break
            
        # get sensor data (only when user leave control page)
        if mode == 'v':
            global humidity
            global temperature
            global gasValue

            humidity = int(data[0])
            temperature = int(data[1])
            gasValue = float(data[2])
            
            motor.changePWM(40)
            break
        # get direction
        elif mode == 'd':
            if data == 'w':
                motor.move('forward')
            elif data == 'a':
                motor.move('turnleft')
            elif data == 's':
                motor.move('backward')
            elif data == 'd':
                motor.move('turnright')
            elif data == 'q':
                motor.move('circleleft')
            elif data == 'e':
                motor.move('circleright')
            elif data == 'x':
                motor.move('stop')
            print('dir=', data)
        # get speed
        elif mode == 's':
            motor.changePWM(speed[int(data)])
            print('speed=', data)


def randomMove():
    char = getChar()
    if (char == '活潑') or (char == '搞怪') or (char == '欠揍'):
        num = random.choice([50, 95, 180, 250])
    elif (char == '沉穩') or (char == '溫柔'):
        num = random.choice([100, 155, 250, 300])
    elif char == '傲嬌':
        num = random.choice([75, 125, 200, 300])
    return num


def adjustDir():
    print('adjust dir')
    motor.move('backward')
    time.sleep(1)
    motor.move('circleright')
    time.sleep(1)


def auto():
    global disList_R
    global disList_L
    currDis_R = round(sensor.getDistanceRight())
    currDis_L = round(sensor.getDistanceLeft())
    #print("R: ", currDis_R, "L: ", currDis_L)

    if (currDis_R > dangerDis) and (currDis_L > dangerDis):
        motor.move('forward')
        time.sleep(longTime)
    elif (currDis_R > warningDis):
        motor.move('turnright')
        time.sleep(shortTime)
    elif (currDis_L > warningDis):
        motor.move('turnleft')
        time.sleep(shortTime)
    else:
        if (currDis_R < dangerDis) or (currDis_L < dangerDis):
            motor.move('backward')
            time.sleep(longTime)
        if (currDis_R >= currDis_L):
            motor.move('circleright')
            time.sleep(longTime)
        else:
            motor.move('circleleft')
            time.sleep(longTime)

    # judged as not moving
    disList_R.append(currDis_R)
    disList_L.append(currDis_L)
    if (disList_R.count(currDis_R) > 2) or (disList_L.count(currDis_L) > 2):
        adjustDir()
        disList_R.clear()
        disList_L.clear()
    elif (len(disList_R) > 15) or (len(disList_L) > 15):
        disList_R.clear()
        disList_L.clear()


def circle():
    movement = random.choices(['circleright', 'circleleft'], weights=[0.7, 0.3], k=1)
    print('move ', movement)
    motor.move(movement[0])
    time.sleep(longTime)
    

# In[3]:


# modify global data
def modifySensorData():
    mode, data = arduinoData()
    if mode == 'n':
        pass
    elif mode == 'v':
        global humidity
        global temperature
        global gasValue

        humidity = int(data[0])
        temperature = int(data[1])
        gasValue = float(data[2])
        #print(humidity, temperature, gasValue)


# count timed on range
def camTimedOnRange():
    camStart, camEnd = getCamTime()

    start = camStart.split(':')
    start = list(map(int, start))
    end = camEnd.split(':')
    end = list(map(int, end))

    # count time
    if start[0] == start[1] and start[1] == end[0] and end[0] == end[1] and end[1] == 0:
        pass
    elif start[0] > end[0] or (start[0] == end[0] and start[1] > end[1]):
        duration = 1440 - ((60 * start[0] + start[1]) - (60 * end[0] + end[1]))
    else:
        duration = (60 * end[0] + end[1]) - (60 * start[0] + start[1])
    cur = time.localtime()
    if start[0] == start[1] and start[1] == cur.tm_min and cur.tm_hour == cur.tm_min and cur.tm_min == 0:
        pass
    elif start[0] > cur.tm_hour or (start[0] == cur.tm_hour and start[1] > cur.tm_min):
        diff = 1440 - ((60 * start[0] + start[1]) -
                       (60 * cur.tm_hour + cur.tm_min))
    else:
        diff = 60 * (cur.tm_hour-start[0]) + cur.tm_min-start[1]
    return duration, diff


# In[4]:


# get userdata from firebase
def getWalkMode(flag):
    walkMode = database.child('USERDATA').child('WalkMode').get().val()
    if flag:
        circleMode = database.child('USERDATA').child('CircleMode').get().val()
        adding = database.child('USERDATA/TakePicture').child('Adding').get().val()
        return walkMode, circleMode, adding
    else:
        return walkMode


def getChar():
    char = database.child('USERDATA').child('Char').get().val()
    return char


def getCamMode():
    camMode = database.child('USERDATA').child('CamMode').get().val()
    camTimedOn = database.child('USERDATA').child('CamTimedOn').get().val()
    return camMode, camTimedOn


def getCamTime():
    camStart = database.child('USERDATA').child('CamStart').get().val()
    camEnd = database.child('USERDATA').child('CamEnd').get().val()
    return camStart, camEnd


def getRetrain():
    retrain = database.child('USERDATA').child('Retrain').get().val()
    return retrain


# In[5]:


# upload to firebase
def uploadHT(h, t, Date, Time):
    try:
        database.child('DHT').child(Date).child(
            Time).update({'Humidity': h, 'Temperature': t})
        print('upload HT success')
    except:
        print('upload HT failed')


def uploadGas(gasStr, gasVal, Date, Time):
    try:
        database.child('GAS').child(Date).child(Time).update(
            {'Gas': gasStr, 'GasValue': gasVal})
        print('upload gas success')
    except:
        print('upload gas failed')


def uploadSensor():
    # current time
    Date = "{}".format(time.strftime("%Y-%m-%d"))
    Time = "{}".format(time.strftime("%H:%M:00"))

    uploadHT(humidity, temperature, Date, Time)

    if gasValue < 0.40:
        gasStr = 'SAFE'
    elif gasValue < 0.60:
        gasStr = 'WARNING'
    else:
        gasStr = 'DANGER'
    uploadGas(gasStr, gasValue, Date, Time)


def uploadRetrain():
    try:
        database.child('USERDATA').update({'Retrain': 'off'})
        print('upload retrain success')
    except:
        print('upload retrain failed')


# In[6]:


# download image for face recognition
def downloadImage(path):
    img_name = database.child('CAMERA/Image').get().val()
    time.sleep(1)
    storage.child('image/' + img_name).download(path + img_name[4:])
    return img_name[4:]


# upload predict result to firebase
def uploadPredictResult(target, num, image_name):
    image_name = 'img_' + image_name
    try:
        database.child('CAMERA').child(target).update({num: image_name})
        print('upload predict result success')
    except:
        print('upload predict result failed')


# In[7]:


def init():
    try:
        motor.init()
        sensor.init()
        modifySensorData()
        uploadSensor()
    except:
        return False
    else:
        return True
    

if __name__ == '__main__':
    init()
    control()
