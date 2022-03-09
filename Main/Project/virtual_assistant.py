# In[1]:


import time
import re
import random
import response as resp
import database as db
import RPi.GPIO as GPIO
import speech_recognition as sr
from gtts import gTTS
from google_trans_new import google_translator
from pydub import AudioSegment
from pydub.playback import play
from omxplayer.player import OMXPlayer
import threading
import ctypes

# speech recognizer
r = sr.Recognizer()
r.energy_threshold = 4000
DEVICE = 2
CHUNK = 1024
RATE = 48000

# google translator
translator = google_translator()

speakFlag = False
cmdFlag = False
part = True
greetFlag = True
greetHour = int(time.strftime('%M')) + 1
warnFlag = True
respFlag = ''
target = ''
LED = 13
light = None


# In[2]:


# save response audio
def contentToAudio(content):
    tts = gTTS(content, lang='zh-TW', slow=False)
    while True:
        try:
            tts.save("/home/pi/Music/resp.mp3")
            break
        except Exception as ex:
            print(ex)
        time.sleep(0.1)
    
    sound = AudioSegment.from_mp3("/home/pi/Music/resp.mp3")
    sound.export("/home/pi/Music/resp.wav", format="wav")


def translate(content, language):    
    result = translator.translate(content, lang_tgt=language)
    tts = gTTS(result, lang=language, slow=False)
    while True:
        try:
            tts.save("/home/pi/Music/resp.mp3")
            break
        except Exception as ex:
            print(ex)
        time.sleep(0.1)

    sound = AudioSegment.from_mp3("/home/pi/Music/resp.mp3")
    sound.export("/home/pi/Music/resp.wav", format="wav")
    

# In[3]:


# folder path for common response 
def folderChoose():
    char = db.getChar()
    if char == '活潑':
        path = 'active'
    elif char == '搞怪':
        path = 'funny'
    elif char == '沉穩':
        path = 'mature'
    elif char == '傲嬌':
        path = 'tsundere'
    elif char == '溫柔':
        path = 'gentle'
    elif char == '欠揍':
        path = 'naughty'
    return path


def speaker(respFlag, target):
    global speakFlag
    try:
        if respFlag:
            charFolder = folderChoose()
            path = '/home/pi/Music/common_resp/' + charFolder + '/' + target + '.wav'
        else:
            path = '/home/pi/Music/resp.wav'
        
        player = OMXPlayer(path, args=['--vol', '-200'])
        speakFlag = False
    except Exception as ex:
        print(ex)
        
    
# In[4]:


# listen to little PI wake up content: 'hey NEMO'
def wakeUp():
    try:
        with sr.Microphone(device_index=DEVICE, chunk_size=CHUNK, sample_rate=RATE) as source:
            r.adjust_for_ambient_noise(source, duration=0.1)
            audio = r.listen(source)
        return r.recognize_google(audio, language='en-US')
    except:
        return ''
    

def callNEMO():
    global cmdFlag
    global speakFlag
    global respFlag
    global target

    lightOff()
    content = wakeUp()
    searchFlag = re.search(r'\b(emo|nemo|anymore|mall)\b', content, flags=re.IGNORECASE)
    if searchFlag is not None:
        cmdFlag = True
        speakFlag = True
        respFlag = True
        target = 'wakeup'
    else:
        cmdFlag = False
        speakFlag = False
        respFlag = ''
        target = ''
    resp.mark = ''

# listen to user request
def listener():
    try:
        with sr.Microphone(device_index=DEVICE, chunk_size=CHUNK, sample_rate=RATE) as source:
            r.adjust_for_ambient_noise(source, duration=0.1)
            print('start listening')
            lightOn()
            audio = r.listen(source, timeout=20.0)
        return r.recognize_google(audio, language='zh-TW')
    except:
        return ''


def listenRequest(q, m):
    global cmdFlag
    global speakFlag
    global respFlag
    global target
    global part
    
    # first conversation
    if part:
        time.sleep(1.5)
        content = listener()
        print('first command:', content)
    
        respFlag, target = resp.getResp(content, part)
        if not respFlag:
            contentToAudio(target)
        print('resp:', respFlag, target)
        print('mark:', resp.mark)
        
        if resp.mark == 'music':
            # push keyword for music search
            q.put_nowait(content)
            # stop camera
            m.value = 0
            cmdFlag = False
            part = True
        elif resp.mark == 'closeBrowser':
            cmdFlag = False
            part = True  
        elif resp.mark != '':
            cmdFlag = True
            part = False
        else:
            cmdFlag = False
            part = True
        
        speakFlag = True
    # second conversation
    else:
        # keep listening
        time.sleep(2.5)
        content = listener()
        print('second command:', content)

        respFlag, target = resp.getResp(content, part)
        print('resp:', respFlag, target)
        print('mark:', resp.mark)
        
        if 'trans' in resp.mark:
            try:
                lang = resp.mark.split(',')[1]
                translate(content, lang)
            except Exception as ex:
                print(ex)
        else:
            try:
                if not respFlag:
                    contentToAudio(target)
            except Exception as ex:
                print(ex)
              
        if target == 'donot_hear':
            cmdFlag = True
            part = False
        else:
            cmdFlag = False
            part = True
            
        speakFlag = True
                     
def autoResp():
    global greetFlag
    global greetHour
    global warnFlag
    
    nowH = int(time.strftime('%H'))
    nowM = int(time.strftime('%M'))
    if (nowH == greetHour) and (nowM == 5):
        if greetFlag:
            greetContent = resp.greeting()
            while True:
                greetHour = random.randint(7, 21)
                if greetHour != nowH:
                    break
            greetFlag == False
            return False, greetContent
    else:
        greetFlag == True

    if (nowM % 10 == 0):
        if warnFlag:
            # get detected sensor data from firebase per 10 minutes
            h, t = db.getHT()
            g = db.getGas()
            warnContent = resp.warn(h, t, g)
            warnFlag = False
            return False, warnContent
    else:
        warnFlag = True
    
    return True, ''
            
            
# In[5]:


# terminate thread
def timeOut_call(thread):
    #print('terminated thread:', thread.name, ', id:', thread.ident)
    if not thread.is_alive():
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# In[6]:


def lightOff():
    global light
    
    try:
        light.ChangeDutyCycle(0)
    except Exception as ex:
        print(ex)
       
       
def lightOn():
    global light
    
    try:
        light.ChangeDutyCycle(60)
    except Exception as ex:
        print(ex)

# In[7]:


def init():
    global speakFlag
    global cmdFlag
    global part
    global greetFlag
    global greetHour
    global warnFlag
    global LED
    global light
    
    speakFlag = False
    cmdFlag = False
    part = True
    greetFlag = True
    greetHour = int(time.strftime('%H')) + 1
    warnFlag = True
    LED = 13
    
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT)
    light = GPIO.PWM(LED, 50)
    light.start(0)

# In[6]:


def start(q, m):
    init()
    global respFlag
    global target

    while True:            
        try:
            # when Nemo say something
            if speakFlag:
                speaker(respFlag, target)
            else:
                respFlag, target = autoResp()
                if respFlag:
                    # print('cmdFlag:', cmdFlag, ', part:', part)
                    # start cmd_thread if user has waked up NEMO
                    if cmdFlag:
                        m.value = 0
                        cmd_thread = threading.Thread(target=listenRequest, name='cmd', args=(q, m,))
                    
                        cmd_thread.start()
                        cmd_thread.join(timeout=20.0)
                        timeOut_call(cmd_thread)
                    # otherwise start wake_thread
                    else:
                        if m.value == 0:
                            m.value = 1
                        wake_thread = threading.Thread(target=callNEMO, name='wake')
                        
                        wake_thread.start()
                        wake_thread.join(timeout=10.0)
                        timeOut_call(wake_thread)
                else:
                    contentToAudio(target)

        except Exception as ex:
            print(ex)
        continue
    
    
if __name__ == '__main__':
    init()
    respFlag, target = autoResp()
    print(respFlag)
    print(target)
    