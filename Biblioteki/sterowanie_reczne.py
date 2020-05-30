import time
from pololu_drv8835_rpi import motors, MAX_SPEED
from servo import *
import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    initServo()
    angle = 0
    speed = 0
    while True:
        char=screen.getch()
        if char == ord('q'):
            speed=0
            angle=0
            break
        elif char == curses.KEY_UP:
            print("accelerate")
            if speed < MAX_SPEED:
                speed = speed+30
        elif char == curses.KEY_DOWN:
            print("slow down")
            if speed > -MAX_SPEED:
                speed = speed-30
        elif char == curses.KEY_LEFT:
            print("Turning left")
            if angle > -50:
                angle = angle - 10
        elif char == curses.KEY_RIGHT:
            print("Turninrg right")
            if angle < 50:
                angle = angle + 10
        elif char == 32:
            speed = 0
            print("stop")
        print(f"Speed {speed}")
        print(f"Angle {angle}")
        motors.setSpeeds(speed, speed)
        setAngle(angle)
finally:
    motors.setSpeeds(0, 0)
    setAngle(0)
    curses.nocbreak()
    curses.endwin()
