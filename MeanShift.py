import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

lower_yellow = np.array([34,0,0])
upper_yellow = np.array([55,255,255])

# setup initial location of window
r,h,c,w = 250,90,400,90 # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
       ret ,frame = cap.read()
       if ret == True:
           hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
           dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

           # apply meanshift to get the new location
           ret, track_window = cv2.meanShift(dst, track_window, term_crit)

           # Draw it on image
           x,y,w,h = track_window
           img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
           img2 = cv2.circle(frame, (x+w/2, y+h/2), 10, (0, 0, 255), -1)

           cv2.imshow('img2',img2)
           k = cv2.waitKey(60) & 0xff#delay function

           if k == 27:
               break
       else:
          break

cv2.destroyAllWindows()
cap.release()