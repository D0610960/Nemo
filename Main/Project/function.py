# In[1]:


import RPi.GPIO as GPIO
from omxplayer.player import OMXPlayer
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import calendar
import datetime
import time
import re
import math
import random
import os
import database as db
import response as resp
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import http.client

chToInt = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
           '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
enToInt = {'Mon': 0, 'Tue': 1, 'Wed': 2,
           'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
weekDict = {'一': 'Mon', '二': 'Tue', '三': 'Wed',
            '四': 'Thu', '五': 'Fri', '六': 'Sat', '日': 'Sun'}

# global variables
driver = None
BUTTON = 23


# In[2]:


def checkDate(tempYear, tempMonth, tempDay):
    tempYear = int(tempYear)
    tempMonth = int(tempMonth)
    tempDay = int(tempDay)
    
    while True:
        lastDay = calendar.monthrange(tempYear, tempMonth)[1]     
        if lastDay < tempDay:
            tempMonth += 1
        else:
            break
    
    newDate = str(tempYear) + '-' + str(tempMonth) + '-' + str(tempDay)
    return newDate


# get time string for setting new alarm or memo
def getDate(dateContent, setTime, repeat):
    now = datetime.datetime.now()
    currYear = now.year
    currMonth = now.month
    currDay = now.day
    currTime = time.strptime(
        str(now.hour)+str(now.minute), '%H%M')

    tempYear = currYear
    tempMonth = currMonth
    tempDay = currDay
    tempTime = time.strptime(setTime, '%H:%M')

    dateFilter = re.findall(r"\d+", dateContent)
    if repeat[0] != '':
        # every month
        tempDay = int(dateFilter[0])
        if tempDay < currDay or (tempDay == currDay and tempTime < currTime):
            if currMonth == 12:
                tempYear += 1
                tempMonth = 1
            else:
                tempMonth += 1
    else:
        # fixed date
        if len(dateFilter) > 1:
            tempMonth = dateFilter[0]
            tempDay = dateFilter[1]
        # next month
        else:
            if currMonth == 12:
                tempMonth = str(1)
            else:
                tempMonth = str(currMonth + 1)
            tempDay = dateFilter[0]
        tempDate = time.strptime(tempMonth + tempDay, '%m%d')
        currDate = time.strptime(str(currMonth) + str(currDay), '%m%d')
        if tempDate < currDate or (tempDate == currDate and tempTime < currTime):
            tempYear += 1
            
    # check last day of tempMonth
    setDate = checkDate(tempYear, tempMonth, tempDay)
    return setDate                                                 


# In[3]]:


# string process for delete alarm or memo
def numberProc(content):
    subNum = re.sub('[第個]', '', content)
    index = 0
    try:
        if subNum == '二十':
            return 20
        else:
            for number in subNum:
                if number is None:
                    index = int(subNum)
                    break
                index += chToInt.get(number)
            return index
    except:
        return False


# string process for add alarm or memo
def datetimeProc(content):
    '''
    # (week) 每天/每週x/每週末
    # (date, freq = T) 每個月x號
    # (date, freq = F) x月x號/下週x/後天
    # (none) 無/明天
    # (time) 凌晨/上午/早上/中午|下午/傍晚/晚上 x點/x點x分
    '''
    setTime = ''
    setDate = ''
    week = []
    repeat = []

    if '周' in content:
        content = content.replace('周', '週')
    
    result = re.search('凌晨|上午|早上|中午|下午|傍晚|晚上', content)
    if result:
        timeIndex = result.span()
        timeContent = content[timeIndex[1]:]
        dateContent = content[:timeIndex[0]]
    else:
        return False
    
    # time string
    timeFilter = re.findall(r"\d+\.?\d*", timeContent)
    if ('下午' in content) or ('傍晚' in content) or ('晚上' in content):
        setHour = str(int(timeFilter[0]) + 12)
    else:
        setHour = str(timeFilter[0])
    if len(timeFilter) == 1:
        setTime = setHour.zfill(2) + ':00'
    else:
        setTime = setHour.zfill(
            2) + ':' + str(timeFilter[1]).zfill(2)
    
    # date string
    if '每天' in dateContent:
        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    elif '每週' in dateContent:
        dayIndex = re.search('每週', dateContent).span()
        week.append(weekDict.get(dateContent[dayIndex[1]:]))
    elif '每週末' in dateContent:
        week = ['Sat', 'Sun']
    elif ('月' in dateContent) and ('號' in dateContent):
        week.append("")
        dateIndex = re.search(r'(?:每個月|下個月|\d+月)\d+號', content).span()
        dateContent = dateContent[dateIndex[0]:]
        if dateContent[0] == '每':
            repeat.append("yes")
        else:
            repeat.append("")
        setDate = getDate(dateContent, setTime, repeat)
    elif '明天' in dateContent:
        week.append("")
    elif '後天' in dateContent:
        week.append("")
        setDate = (datetime.datetime.now() +
                datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    elif '週' in dateContent:
        week.append("")
        dateIndex = re.search(r'(?:下|這|)週', content).span()
        dateContent = dateContent[dateIndex[0]:]
        if len(dateContent) > 3:
            setDate = 'multi'
        else:
            offset = enToInt.get(weekDict.get(dateContent[-1]))
            if dateContent[0] == '下':
                diff = 7 - datetime.date.today().weekday() + offset
            else:
                diff = offset - datetime.date.today().weekday()

            setDate = (datetime.datetime.now() +
                    datetime.timedelta(days=diff)).strftime('%Y-%m-%d')
    else:
        week.append("")
    
    return (setDate, setTime, week, repeat)
            
        
# string process for play music
def musicProc(content):
    global driver
    openBrowser = False
    
    if ('要聽' in content) or ('想聽' in content):
        musicIndex = re.search(r'(?:要|想)聽', content).span()
        content = content[musicIndex[1]:]
        openBrowser = playVideo(content)
    elif (content == '關閉音樂') or (content == '關掉音樂'):
        driver.quit()
    return openBrowser
        
    
# In[4]:


# alarm ringing
def playRing(alarmSound):
    try:
        player = OMXPlayer('/home/pi/Music/alarm/' + alarmSound +
                           '.mp3', args=['--loop', '--vol', '-620'])
        count = 0

        while True:
            if GPIO.input(BUTTON):
                pass
            # button pressed
            else:
                count += 1
                # long press for 3s to quit
                if count > 30:
                    print('end')
                    player.quit()
                    break
            time.sleep(0.1)
    except Exception as ex:
        print(ex)


# save memo audio
def memoAudio(content):
    tts = gTTS(content, lang='zh-TW', slow=False)
    while True:
        try:
            tts.save("/home/pi/Music/memo/remind.mp3")
            break
        except Exception as ex:
            print(ex)
        time.sleep(0.1)

    sound = AudioSegment.from_mp3("/home/pi/Music/memo/remind.mp3")
    sound.export("/home/pi/Music/memo/remind.wav", format="wav")


# memo reminding
def reminder(memoText):
    nickname = db.getNickname()
    content = nickname + '，該' + memoText
    content = resp.combine(content, 'r')
    memoAudio(content)
    try:
        player = OMXPlayer('/home/pi/Music/memo/remind.wav',
                           args=['--loop', '--vol', '-620'])
        count = 0

        while True:
            if GPIO.input(BUTTON):
                pass
            # button pressed
            else:
                count += 1
                # long press for 3s to quit
                if count > 30:
                    print('end')
                    player.quit()
                    break
            time.sleep(0.1)
    except Exception as ex:
        print(ex)


# In[5]:


# get first video without video list
def getVideoID():
    videoID = ''
    last = None
    elems = driver.find_elements_by_tag_name('a')
    for elem in elems:
        href = elem.get_attribute('href')
        if href is None:
            pass
        else:
            videoID = re.search("v=(.*)", href)
        if videoID:
            videoID = videoID.group(1)
            # drop duplicated ID
            if videoID == last or re.search('list', videoID):
                continue
            last = videoID
            break
    return videoID


def playVideo(query):
    global driver
    
    try:
        if checkInternet():
            # set chrome options
            option = webdriver.ChromeOptions()
            option.add_argument('--disable-notifications')
            option.add_argument('--disable-gpu')
            option.add_argument('blink-settings=imagesEnabled=false')
            #option.add_argument('--headless')

            # open chrome driver 
            driver = webdriver.Chrome(
                "/usr/lib/chromium-browser/libs/chromedriver", options=option)
            driver.maximize_window()
            # search by query content
            url = 'https://www.youtube.com/results?search_query=' + \
                urllib.parse.quote(query.encode('utf8'))
            driver.get(url)
            # choose video
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@href='/watch?v=" + getVideoID() + "']"))).click()
            # do not play next video
            return True
        else:
            driver.quit()
            return False
    except:
        return False


# In[5]:


# check wifi connect
def checkInternet():
    url = "www.youtube.com"
    conn = http.client.HTTPConnection(url, timeout=10)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        return False
    
    
# turn off auto play switch
def autoCloseDriver():
    global driver

    # video end
    try:
        driver.find_element_by_xpath("//button[@title='重播']")
        return True
    except:
        pass
    
    # connect failed
    if checkInternet():
        pass
    else:
        return True
    
    # page crash
    return False

# button close driver
def buttonCloseDriver():
    global driver
    
    if GPIO.input(BUTTON):
        return False
    # button pressed
    else:
        driver.quit()
        print('close music')
        return True


# turn off auto play switch
def nextVideoOff():
    global driver
    
    # remove the element which blocks the switch
    try:
        driver.find_element_by_xpath("//*[@aria-label='我知道了']").click()
    except:
        pass
    
    #turn off switch
    try:
        driver.find_element_by_xpath("//*[@aria-label='自動播放'][@aria-pressed='true']").click()
        return 1
    except:
        return 0
    
    
# open settings menu
def settingMenu():
    global driver

    # remove the element which blocks the settings button
    try:
        driver.find_element_by_xpath("//ytd-button-renderer[@id='dismiss-button']").click()  
    except:
        pass
    
    try:
        # click settings button
        driver.find_element_by_class_name("ytp-settings-button").click()
        
        # found menu element
        menu = driver.find_elements_by_css_selector(".ytp-menuitem-label")
        found = False
        for i in range (len(menu)):
            if menu[i].text == '畫質':
                menu[i].click()
                found = True
                break
        
        # if found quality item, set the lowest quality
        if found:
            quality = driver.find_elements_by_css_selector(".ytp-menuitem-label")
            quality[-2].click()
            return -1
        # otherwise close settings menu
        else:
            driver.find_element_by_class_name("ytp-settings-button").click()
            return 1
    except:
        return 1
    
    
# detect AD element
def checkAD():
    global driver
    
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-ad-player-overlay")))
        #driver.find_element_by_class_name("ytp-ad-player-overlay")
        found = True
    except:
        found = False
        
    if found:
        try:
            driver.find_element_by_class_name("ytp-ad-skip-button").click()
        except:
            pass
        return True
    else:
        return False
    
# In[6]:


def init():
    global driver
    global BUTTON

    driver = None
    BUTTON = 23
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    except:
        return False
    else:
        return True

# In[7]:

if __name__ == '__main__':
    init()
    db.adjustVol()
    
    try:
        s = '我要聽周深的曇花一現'
        openBrowser = musicProc(s)
        setState = 0
        
        while True:
            if autoCloseDriver():
                openBrowser = False
            elif buttonCloseDriver():
                openBrowser = False
            else:
                if checkAD():
                    pass
                else:
                    # have not set video
                    if setState != -1:
                        if setState == 0:
                            setState = nextVideoOff()
                        elif setState == 1:
                            setState = settingMenu()
                    else:
                        pass 
    except Exception as ex:
        print(ex)
    finally:
        if driver is not None:
            openBrowser = False
