import RPi.GPIO as GPIO
import time

def getDistanceRight():
    try:
        GPIO.output(TRIG_R, False)
        time.sleep(0.001)
        GPIO.output(TRIG_R, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_R, False)

        while GPIO.input(ECHO_R) == 0:
            start = time.time()

        while GPIO.input(ECHO_R) == 1:
            end = time.time()

        return (end - start) * 17150
    except:
        return False

def getDistanceLeft():
    try:
        GPIO.output(TRIG_L, False)
        time.sleep(0.001)
        GPIO.output(TRIG_L, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_L, False)

        while GPIO.input(ECHO_L) == 0:
            start = time.time()

        while GPIO.input(ECHO_L) == 1:
            end = time.time()

        return (end - start) * 17150
    except:
        return False

def init():
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        global TRIG_R
        global ECHO_R
        global TRIG_L
        global ECHO_L

        TRIG_R = 22
        ECHO_R = 23
        TRIG_L = 17
        ECHO_L = 18

        GPIO.setup(TRIG_R, GPIO.OUT)
        GPIO.setup(ECHO_R, GPIO.IN)
        GPIO.setup(TRIG_L, GPIO.OUT)
        GPIO.setup(ECHO_L, GPIO.IN)
        
        return True
    except:
        return False
    else:
        return True
    
    
if __name__ == '__main__':
    try:
        init()
        print(getDistanceLeft())
        print(getDistanceRight())
        
    except:
        print('Close Program')
    finally:
        print('Close Program')
        GPIO.cleanup()

