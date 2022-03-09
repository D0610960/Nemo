# In[1]:


import cv2
import os
import time
import datetime
import database as db
import warnings
warnings.filterwarnings('ignore')

cap = None
interval = 20

# In[2]:


def checkCamera():
    global cap

    if cap is None:
        cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #print('camera restart...')

    if not cap.isOpened():
        #print('camera reopen...')
        cap.open(0)


def closeCamera():
    global cap

    if cap is not None:
        cap.release()
        cap = None
        #print('camera close...')
        

# In[3]:


def realTimeImage():
    global cap
    success = False

    currentTime = str(time.strftime('%H%M%S'))
    if int(currentTime[-2:]) % interval == 0:
        while True:
            checkCamera()
            rval, frame = cap.read()
            cv2.waitKey(33)
            if rval:
                img_path = './camera/img_' + currentTime + '.jpg'
                cv2.imwrite(img_path, frame)
                success = db.uploadImg(img_path)

            if success:
                #print('uploaded real time image')
                closeCamera()
                break
    else:
        closeCamera()


def faceImage(imageNum, memberName):
    global cap
    success = False

    while True:
        checkCamera()
        time.sleep(1)
        rval, frame = cap.read()
        cv2.waitKey(33)
        if rval:
            img_path = './new_member/' + imageNum + '.jpg'
            cv2.imwrite(img_path, frame)
            success = db.uploadfaceImage(img_path, imageNum, memberName)

        if success:
            #print('added face image of new member')
            closeCamera()
            break


# In[4]:


def start(m):
    cnt = 0
    
    while True:
        try:
            if m.value:
                pass
            else:
                # clear real time images
                if(cnt == 50):
                    os.system(
                        "rm -rf /home/pi/Project/camera/*.jpg")
                    cnt = 0
                else:
                    pass

                camMode, camTimedOn = db.getCamMode()
                imageNum, memberName, adding = db.getTakePicture()

                # add face image of new member
                if imageNum != '0':
                    faceImage(imageNum, memberName)
                else:
                    # if camera mode is on
                    if camMode == 'on':
                        realTimeImage()
                        cnt += 1
                    # if camera mode is off
                    else:
                        # if timed on mode is on
                        if camTimedOn == 'on':
                            duration, diff = db.camTimedOnRange()
                            # if in time range
                            if duration > diff:
                                realTimeImage()
                                cnt += 1
                            else:
                                closeCamera()
                        else:
                            closeCamera()
                    # print(cnt)
        except:
            pass
        continue
    

# In[5]:


if __name__ == '__main__':
    while True:
        checkCamera()
        time.sleep(1)