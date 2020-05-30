import time
import random
from pololu_drv8835_rpi import motors, MAX_SPEED
from servo import *
from linie import *
    
def get_angle(frame):
    #print(frame.shape)
    height, width, _ = frame.shape

    lines = detect_lane(frame)
    img_w_lines = draw_lines(frame, lines)

    cv2.imshow("linie", img_w_lines)

    i = 0
    #print(len(lines))
    new_lines = []
    #sprawdzmy czy widzimy poziome linie - prawdopodobnie sa one bledne. Jesli taka jest to ja ignorujmy
    if len(lines) >0 :
        for line in lines:
            x1, _, x2, _ = line[0]
            if abs((height/3)/(x2-x1))  > 0.2:
                new_lines.append(line[0])
                i+=1
            else:
                print("Odrzucam pozioma linie!")
        lines = [[new_line] for new_line in new_lines]
                
    if len(lines) == 0:
        return 0
    
    if len(lines)  == 1:
        x1, _, x2, _ = lines[0][0]
        
        dx = x2 - x1
        dy = int(height*1/2)
        
    if len(lines) == 2:
        #print(lines[0][0])
        #print(lines[1][0])
        _,_, xl, _ = lines[0][0]
        _,_, xr, _ = lines[1][0]
        
        mid = 1/2 * width
        
        dx = (xl + xr)/2 - mid
        dy = int(height*1/2) 
        
        
    angle = math.atan2(dx, dy)
    angle = 180 * angle / 3.14
    #print(angle)
    return angle



if __name__ == "__main__":
    a = 0
    newA = 0
    oldA = 0
    lt=0
    speed = 0
    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    #cap.set(15, -8.0)
    
    initServo()
    setAngle(0)
    motors.setSpeeds(speed,speed)
    try:
        while True:
            if(cap.isOpened()):
                ct = time.time()
                dt = ct - lt
                fps = 1/dt
                #print(f"fps {fps}")
                ret, frame = cap.read()
                
                #cv2.imwrite("/home/pi/TOFIC/image1.png", frame )
                #exit()
                if ret:
                    newA = get_angle(frame)
                    #print(params[0])
                    if newA is not None:
                        a = a + 0.25*(newA-a)      #  + correct(a, params)
                        if a<40 and a>-40:
                            setAngle(a)
                        elif a<-40:
                            setAngle(-40)
                        else:
                            setAngle(40)
                        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                ##motors.setSpeeds(90,90)
                lt = ct

        cap.release()
        cv2.destroyAllWindows()
    finally:
        motors.setSpeeds(0 ,0)
