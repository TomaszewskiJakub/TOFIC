# Import libraries
import RPi.GPIO as GPIO
import time

servo1 = None

def initServo():
    global servo1
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    #Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(40,GPIO.OUT)
    servo1 = GPIO.PWM(40,50) # Note 11 is pin, 50 = 50Hz pulse

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    print ("Waiting for 2 seconds")
    time.sleep(2)

def setAngle(angle):
    global servo1
    tmp = 6.5 + angle * 1.5 / 50
    servo1.ChangeDutyCycle(tmp)
    #time.sleep(0.5)
    #servo1.ChangeDutyCycle(0)

if __name__ == "__main__":
    initServo()
    #for i in range(-50, 51, 10):
    #    SetAngle(i)
    #    time.sleep(1)

    setAngle(0)

    servo1.stop()
    GPIO.cleanup()





