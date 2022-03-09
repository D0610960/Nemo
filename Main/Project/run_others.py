# In[1]:


import time
import function as func
import database as db


# In[2]:


def start(q, m):
    db.uploadWeather()
    func.init()
    openBrowser = False
    setState = 0
    
    while True:
        try:
            # get one week weather information
            if time.strftime('%H:%M') == '06:00':
                db.uploadWeather()
                
            # music control
            if not q.empty():
                db.adjustVol()
                openBrowser = func.musicProc(q.get())
                setState = 0
                m.value = 2
                
            # automatically check video
            if openBrowser:
                if func.autoCloseDriver():
                    openBrowser = False
                elif func.buttonCloseDriver():
                    openBrowser = False
                else:
                    if func.checkAD():
                        pass
                    else:
                        # have not set video
                        if setState != -1:
                            if setState == 0:
                                setState = func.nextVideoOff()
                            elif setState == 1:
                                setState = func.settingMenu()
                        else:
                            m.value = 1
                    
           
            # alarm
            alarmResult = db.alarm()
            if alarmResult != False:
                print('alarm', alarmResult)
                func.playRing(alarmResult)
            # memo
            memoResult = db.memo()
            if memoResult != False:
                print('memo', memoResult)
                func.reminder(memoResult)
                
        except:
            pass
        continue
