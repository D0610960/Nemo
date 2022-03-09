import RPi.GPIO as GPIO
import time

def move(direction):
    if direction == 'stop':
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)
    if direction == 'forward':
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
    if direction == 'backward':
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)
    if direction == 'turnleft':
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
    if direction == 'turnright':
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)
    if direction == 'circleleft':
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
    if direction == 'circleright':
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)
    
    
def changePWM(speed):
    global PWMA
    global PWMB
    
    PWMA.ChangeDutyCycle(speed)
    PWMB.ChangeDutyCycle(speed)
    

def init():

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global ENA
    global ENB
    global IN1
    global IN2
    global IN3
    global IN4
    global PWMA
    global PWMB

    ENA = 12
    ENB = 13
    IN1 = 16
    IN2 = 26
    IN3 = 5
    IN4 = 6

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(ENB, GPIO.OUT)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        PWMA = GPIO.PWM(ENA, 50)
        PWMA.start(40)
        PWMB = GPIO.PWM(ENB, 50)
        PWMB.start(40)
        move('stop')
    except:
        return False
    else:
        return True


if __name__ == '__main__':
    # circleleft turnleft backward
    # circleright turnright forward
    cnt = 0
    try:
        init()
        while True:
            print(cnt)
            
            movement = 'turnright'
            move(movement)
            time.sleep(1)
            
            cnt = 1
            if cnt % 10 == 0:
                changePWM(cnt)
                if cnt == 100:
                    cnt = 0
            
    except KeyboardInterrupt:
        move('stop')
        print('Close Program')
    finally:
        move('stop')
        print('Close Program')
        stopPWM()
        GPIO.cleanup()
