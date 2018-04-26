import cv2
import numpy as np


cap = cv2.VideoCapture(1)

while(cap):
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    lower_blue = np.array([140,50,0])
    upper_blue = np.array([170,255,255])
    grey = cv2.inRange(hsv, lower_blue, upper_blue)
    #immagine in scala di grigi filtrata in un intervallo di tonalita
    #cv2.imshow('rgb',frame) #DEBUG
    #cv2.imshow('hsv',hsv)
    cv2.imshow('grey', grey)

    #Applico una contours detection.
    img2, contours, hierarchy = cv2.findContours(grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 9)
    #cv2.imshow('img2',frame)

    #Applico canny edge detectioin


    #Esc chiude le schermate
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()

