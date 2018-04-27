import cv2
import numpy as np
import math

#Inizializza la capture video
cap = cv2.VideoCapture(0)

#Controlla se salvare le immagini da processare o no
save = True
n = 5
deltaTime = 5000

#Salva n frame in un intervallo delta t
counter = 0
while cap and save:
    ret, frame = cap.read()
    cv2.imwrite(str(counter)+'frame.png',frame)
    counter = counter +1
    if counter == n:
        save = False



