import cv2
import numpy as np
import math

def ROI(img):
    height, width = img.shape
    mask = np.zeros_like(img)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(img, mask)
    #cv2.imshow("cropped", cropped_edges)
    return cropped_edges

def detect_line_segments(cropped_edges):
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 20  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, 
                                    np.array([]), minLineLength=20, maxLineGap=4)
    return line_segments

def make_points(frame, line):
    height, width = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 2 / 3)  # make points from middle of the frame down

    # bound the coordinates within the frame
    try:
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
        return [[x1, y1, x2, y2]]
    except:
        return
    

def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on right 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        #print(f"left {left_fit_average}")
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        #print(f"rigth {right_fit_average}")
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines

def detect_edge(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #lower_blue = np.array([105, 110, 20])
    #upper_blue = np.array([130, 140, 110])
    
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    lower_red1 = np.array([0, 90, 70])
    upper_red1 = np.array([10, 215, 180])
    
    lower_red2 = np.array([170, 90, 70])
    upper_red2 = np.array([179, 215, 180])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    

    mask = mask1 | mask2
    
    #cv2.imshow("mask", mask)
    
    #mask = cv2.morphologyEx(mask, 
                            #cv2.MORPH_CLOSE, 
    #cv2.imshow("mask", mask)                       #np.ones((5,5),np.uint8))

    edges = cv2.Canny(mask, 200, 400)
    
    return edges


def detect_lane(frame):
    edges = detect_edge(frame)
    cropped = ROI(edges)
    lines = detect_line_segments(cropped)
    lane_lines = average_slope_intercept(cropped, lines)

    return lane_lines

def draw_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)
#     while(True):
#         if(cap.isOpened()):
#             ret, frame = cap.read()
#             _, frame = cap.read()
#             if ret:
#                 detect_edge(frame)
#                 #get_angle(frame)
#                 cv2.imshow("Camera", frame)
#                 key = cv2.waitKey(1)
#                 if key == 27:
#                     break
# 
#     cap.release()
#     cv2.destroyAllWindows()

def nothing(x):
    pass

def cos_s(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([0, 70, 118])
    upper_blue = np.array([10, 177, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)


    #cv2.imshow("frame", frame)
    #cv2.imshow("mask", mask)

    edges = cv2.Canny(mask, 200, 400)
    
    return edges
    

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    

    while True:
        _, frame = cap.read()
        detect_edge(frame)
        
        key = cv2.waitKey(1)
        if key == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()
