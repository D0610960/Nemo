# In[1]:


import pyrebase
import urllib.request
import urllib.parse
import information as info
import calendar
import datetime
import time
import os

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


chToInt = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
           '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
enToInt = {'Mon': 0, 'Tue': 1, 'Wed': 2,
           'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
weekDict = {'一': 'Mon', '二': 'Tue', '三': 'Wed',
            '四': 'Thu', '五': 'Fri', '六': 'Sat', '日': 'Sun'}

volume = 50


# In[2]:


# get userdata
def getNickname():
    name = database.child('USERDATA').child('Nickname').get().val()
    return name


def getChar():
    char = database.child('USERDATA').child('Char').get().val()
    return char


def getTempMode():
    temp = database.child('USERDATA').child('TempMode').get().val()
    return temp


def getWalkMode():
    walkMode = database.child('USERDATA').child('WalkMode').get().val()
    return walkMode


def getCamMode():
    camMode = database.child('USERDATA').child('CamMode').get().val()
    camTimedOn = database.child('USERDATA').child('CamTimedOn').get().val()
    return camMode, camTimedOn


def getCamTime():
    camStart = database.child('USERDATA').child('CamStart').get().val()
    camEnd = database.child('USERDATA').child('CamEnd').get().val()
    return camStart, camEnd


def getLocation():
    city = database.child('USERDATA').child('City').get().val()
    dist = database.child('USERDATA').child('Dist').get().val()
    return city, dist


def getTakePicture():
    imageNum = database.child(
        'USERDATA/TakePicture').child('ImageNum').get().val()
    memberName = database.child(
        'USERDATA/TakePicture').child('MemberName').get().val()
    adding = database.child('USERDATA/TakePicture').child('Adding').get().val()
    return imageNum, memberName, adding


# get sensor data
def getHT():
    DHT = database.child('DHT').get().val()
    if DHT is not None:
        day_list = list(DHT.values())
        lastDay = day_list[len(day_list) - 1]
        time_list = list(lastDay.values())
        lastTime = time_list[len(time_list)-1]
        h = lastTime['Humidity']
        t = lastTime['Temperature']
    else:
        h = 'None'
        t = 'None'
    return h, t


def getGas():
    GAS = database.child('GAS').get().val()
    if GAS is not None:
        day_list = list(GAS.values())
        lastDay = day_list[len(day_list) - 1]
        time_list = list(lastDay.values())
        lastTime = time_list[len(time_list)-1]
        g = lastTime['Gas']
    return g


# In[3]:


# upload data or image
def uploadImg(img_path):
    img_name = img_path[-14:]
    try:
        storage.child("image/" + img_name).put(img_path)
        database.child('CAMERA').update({'Image': img_name})
        print('upload real time image success')
        return True
    except Exception as ex:
        print(ex)
        print('upload real time image failed')
        return False


def uploadfaceImage(img_path, imageNum, memberName):
    try:
        storage.child("face/" + memberName + '/' +
                      imageNum + '.jpg').put(img_path)
        content = memberName + ',' + imageNum
        database.child(
            'USERDATA/TakePicture').update({'Upload': content, 'ImageNum': '0'})
        print('upload new member image success')
        return True
    except:
        print('upload new member image failed')
        return False


def uploadWeather():
    city, dist = getLocation()
    dayData = info.getWeather(city, dist, True)
    Date = dayData[0]
    Pop = dayData[1]
    Temp = dayData[2]
    Uvi = dayData[3]
    Ws = dayData[4]
    Wx = dayData[5]
    Aq = info.airQuality(city, dist, True)

    try:
        for i in range(7):
            database.child('WEATHER').child('Day' + str(i+1)).update(
                {'Date': Date[i], 'Wx': Wx[i], 'Pop': Pop[i], 'Uvi': Uvi[i], 'Aq': Aq, 'Ws': Ws[i], 'Temp': Temp[i]})
        print('upload weather information success')
        return True
    except Exception as ex:
        print('upload weather information failed: ', ex)
        return False


# In[4]:


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


# In[5]:


def addAlarm(index):
    setDate = index[0]
    setTime = index[1]
    week = index[2]
    repeat = index[3]
    
    if setDate != '':
        return 'alarm_failed'
    else:
        try:
            database.child('ALARM').push(
                {'AlarmTime': setTime, 'Sound': 'Basic', 'Title': '', 'Week': week, 'Flag': True})
            return 'alarm_success'
        except:
            return 'set_failed'


def addMemo(index, text):
    setDate = index[0]
    setTime = index[1]
    week = index[2]
    repeat = index[3]
    
    if setDate == 'multi':
        return 'memo_failed'
    else:
        try:
            database.child('MEMO').push(
                {'Date': setDate, 'MemoTime': setTime, 'Repeat': repeat, 'Text': text, 'Week': week, 'Flag': True})
            return 'memo_success'
        except:
            return 'set_failed'


def nextMonth(oldDate):
    oldYear = int(oldDate[0:4])
    oldMonth = int(oldDate[5:7])
    oldDay = int(oldDate[8:10])

    if oldMonth == 12:
        newYear = oldYear + 1
        newMonth = 1
    else:
        newYear = oldYear
        newMonth = oldMonth + 1
    
    while True:
        lastDay = calendar.monthrange(newYear, newMonth)[1]
        if lastDay < oldDay:
            newMonth += 1
        else:
            break
    
    newDate = str(newYear) + '-' + str(newMonth) + '-' + str(oldDay)
    return newDate


def modifyMemoDate(key, oldDate):
    newDate = nextMonth(oldDate)
    database.child('MEMO').child(key).update({'Date': newDate})


# delete alarm and memo
def deleteByNo(childName, number):
    try:
        item = database.child(childName).get().val()
        if item is not None:
            key_list = list(item.keys())
            database.child(childName).child(key_list[number-1]).remove()
        if childName == 'ALARM':
            return 'delete_alarm'
        else:
            return 'delete_memo'
    except:
        return 'delete_failed'


def deleteByKey(childName, item):
    try:
        database.child(childName).child(item.key()).remove()
        print('delete succeeded')
    except:
        print('delete failed')


# check number of alarms and memos
def checkAlarm():
    alarm = database.child('ALARM').get().val()
    if alarm is not None:
        return len(alarm)
    else:
        return 0


def checkNote():
    memo = database.child('MEMO').get().val()
    if memo is not None:
        return len(memo)
    else:
        return 0


# In[6]:


# control alarm rining and memo reminding
def changeFlag(childName, key, flag):
    try:
        database.child(childName).child(key).update({'Flag': flag})
        print('change succeeded')
    except:
        print('change failed')


def alarm():
    allAlarm = database.child('ALARM').get()
    if allAlarm.val() != None:
        for alarmKey in allAlarm.each():
            timesUp = alarmKey.val().get('Flag')
            alarmTime = alarmKey.val().get('AlarmTime')
            startTime = str(datetime.datetime.strptime(
                str(datetime.datetime.now())[11:-10], '%H:%M'))[11:-3]

            if startTime != alarmTime:
                if not timesUp:
                    changeFlag('ALARM', alarmKey.key(), True)
                continue
            else:
                if timesUp:
                    alarmWeekList = alarmKey.val().get('Week')
                    alarmSound = alarmKey.val().get('Sound')
                    now = datetime.datetime.now()

                    if ''.join(alarmWeekList) == '':
                        deleteByKey('ALARM', alarmKey)
                        return alarmSound
                    else:
                        for weekday in alarmWeekList:
                            if enToInt.get(weekday) == now.weekday():
                                changeFlag('ALARM', alarmKey.key(), False)
                                return alarmSound
                else:
                    pass
    else:
        pass
    return False


def memo():
    allMemo = database.child('MEMO').get()
    if allMemo.val() != None:
        for memoKey in allMemo.each():
            timesUp = memoKey.val().get('Flag')
            memoTime = memoKey.val().get('MemoTime')
            startTime = str(datetime.datetime.strptime(
                str(datetime.datetime.now())[11:-10], '%H:%M'))[11:-3]

            if startTime != memoTime:
                if not timesUp:
                    changeFlag('MEMO', memoKey.key(), True)
                continue
            else:
                if timesUp:
                    memoWeekList = memoKey.val().get('Week')
                    memoDate = memoKey.val().get('Date')
                    memoRepeat = memoKey.val().get('Repeat')
                    memoText = memoKey.val().get('Text')
                    now = datetime.datetime.now()
                    print('repeat=', memoRepeat)
                    if ''.join(memoDate) != '':
                        if memoRepeat == ['yes'] and memoDate == str(now.date()):
                            changeFlag('MEMO', memoKey.key(), False)
                            modifyMemoDate(memoKey.key(), memoDate)
                            return memoText
                        else:
                            if memoDate == str(now.date()):
                                deleteByKey('MEMO', memoKey)
                                return memoText
                    else:
                        if ''.join(memoWeekList) == '':
                            deleteByKey('MEMO', memoKey)
                            return memoText
                        else:
                            for weekday in memoWeekList:
                                if enToInt.get(weekday) == now.weekday():
                                    changeFlag('MEMO', memoKey.key(), False)
                                    return memoText
                else:
                    pass
    else:
        pass
    return False

# In[7]:


# adjust nemo volume by user setting
def adjustVol():
    global volume

    newVolume = database.child('USERDATA').child('Volume').get().val()
    if volume != newVolume:
        volume = newVolume
        os.system('amixer set Master ' + str(newVolume) + '%')
    else:
        pass
