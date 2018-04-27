import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

while(cap):
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([140,50,0])
    upper_blue = np.array([170,255,255])

    lower_apple = np.array([168,180,80])
    upper_apple = np.array([188,255,200])

    lower_postit = np.array([25,100,180])
    upper_postit = np.array([45,255,255])

    grey = cv2.inRange(hsv, lower_apple, upper_apple)
    #immagine in scala di grigi filtrata in un intervallo di tonalita
    #cv2.imshow('rgb',frame) #DEBUG
    #cv2.imshow('hsv',hsv)
    cv2.imshow('grey', grey)

    #Applico una contours detection.
    #img2, contours, hierarchy = cv2.findContours(grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 9)
    cv2.imshow('frame',frame)

    #Applico hough circle transform per trovare i cerchi nel frame
    circles = cv2.HoughCircles(grey, cv2.HOUGH_GRADIENT, 1, 50 ,param1 = 50, param2 = 30, minRadius = 20, maxRadius = 200)

    #Disegno i cerchi e i centri
    if circles is None:
       cv2.imshow('frame', frame)
       continue

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(frame, (i[0], i[1]), i[2], (0, 0, 255), 1)  # draw the outer circle
        cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)  # draw the center of the circle
    #Esc chiude le schermate0
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()


#return angles in radiants
def inverseCinematic(x, y, z, l1, l2, l3):
    fi = 30 *math.pi/180 #Angolo che definisce l'orientamento della pinza rispetto all'asse x.
    xp = x -l3*math.cos(fi)
    zp = z -l3*math.sin(fi)

    teta2 = math.acos( ((xp*xp + zp*zp -l1*l1-l2*l2)/2*l1*l2))
    teta1 = math.atan2( (-l2*math.sin(teta2)*xp + ((l1+l2*math.cos(teta2))*zp)),((l1+l2*math.cos(teta2))*xp + l2*math.sin(teta2)*zp ))
    teta3 = fi - teta1 - teta2
    teta0 = math.atan2(x,y)
    angoli = [teta0,teta1,teta2,teta3]
    return angoli

def inverseCinematic2(xd, yd, zd, betad, d1,l1,l2,l3,d5):

    teta1 = math.atan2(yd, xd)

    A1 = xd*math.cos(teta1) + yd*math.sin(teta1) - d5*math.cos(betad) -l1
    A2 = d1 - zd - d5*math.sin(betad)

    teta3 = math.acos(((A1*A1 + A2*A2 -l2*l2 -l3*l3)/2*l2*l3))
    teta2 = math.atan2(((l2 + l3*math.cos(teta3))*A2 - l3*math.sin(teta3)*A1),((l2 + l3*math.cos(teta3))*A1 +l3*math.sin(teta3)*A2))
    teta4 = betad - teta2 - teta3 - math.pi/2

    angoli = [teta1, teta2, teta3, teta4]
    return angoli

angoli = inverseCinematic2(0,2,1,0, 0, 0,1,1,1)
i = 0
for angolo in angoli:
    angolo = angolo*180/math.pi
    i = i +1
    print("angolo", i, angolo)
