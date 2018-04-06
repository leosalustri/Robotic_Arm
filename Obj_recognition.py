import cv2
import numpy as np

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


cap = cv2.VideoCapture(0)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([100,50,50])
    upper_blue = np.array([140,255,255])

    lower_yellow = np.array([34,0,0])
    upper_yellow = np.array([55,255,255])


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)

    image, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(opening, contours,-1, (140, 140, 140), 3)
    #Centroid
    cnt = contours[0]
    M = cv2.moments(cnt)

    cy = constrain(int(M['m01'] / M['m00']), 0,540)
    cx = constrain(int(M['m10'] / M['m00']), 0,480 )



    'Debug opening = cv2.drawContours(opening, contours, -1, (145, 145, 130), 3)'
    # Bitwise-AND mask and original image
    'DEBUG res = cv2.bitwise_and(frame,frame, mask= mask)'
    cv2.imshow('frame',frame)
    cv2.imshow('opening',opening)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()

