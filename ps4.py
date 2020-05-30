from pyPS4Controller.controller import Controller, Event
from servo import *
from pololu_drv8835_rpi import motors, MAX_SPEED

import cv2

initServo()
setAngle(0)
class MyController(Controller):
    current = 0
    
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        #self.cap = cv2.VideoCapture(0)
        
    def on_L3_left(self, value):
        setAngle(45*value/32767)
    def on_L3_right(self, value):
        setAngle(45*value/32767)
    def on_L3_at_rest(self):
        print("rest")
        #setAngle(0)
    def on_R1_press(self):
        self.current = self.current + 30
        motors.setSpeeds(self.current,self.current)
    def on_L1_press(self):
        self.current = self.current - 30
        motors.setSpeeds(self.current,self.current)
    def on_R2_press(self, value):
        value = (value + 32767)/2
        motors.setSpeeds(int(400*value/38767), int(400*value/38767))
        self.current = 0
    def on_L2_press(self, value):
        value = (value + 32767)/2
        motors.setSpeeds(int(-400*value/38767), int(-400*value/38767))
        self.current = 0
    def on_R2_release(self):
        motors.setSpeeds(0,0)
        self.current = 0
    def on_L2_release(self):
        motors.setSpeeds(0,0)
        self.current = 0
    def on_x_press(self):
        motors.setSpeeds(0, 0)
        self.controller = 0

        
        

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
#scontroller.on_L3_left()
print(f"Max speed: {MAX_SPEED}")
controller.listen()