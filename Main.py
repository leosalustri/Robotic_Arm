import cv2
import numpy as np
import math

#Inizializza la capture video
cap = cv2.VideoCapture(0)

#Parametri hsv da cercare
lower_red = np.array([140,50,0])#da controllare i valori con le dovute proporzioni.
upper_red = np.array([140,50,0])
lower_blue = np.array([140,50,0])#da controllare i valori con le dovute proporzioni.
upper_blue = np.array([140,50,0])
lower_green = np.array([140,50,0])#da controllare i valori con le dovute proporzioni.
upper_green = np.array([140,50,0])

#Controlla se salvare le immagini da processare o no
save = True
numFrame = 5

#Salva n frame nella directory frame
counter = 0
while cap and save:
    ret, frame = cap.read()
    cv2.imwrite('frame/'+str(counter)+'frame.png',frame)
    counter = counter +1
    if counter == numFrame:
        save = False

#Processo le foto e per ognuna calcolo il HOUG CIRCLE TRANSFORM Tresholdando ai valori hsv richiesti

    foto = cv2.imread( 'frame/0frame.png', cv2.IMREAD_COLOR)#leggo il frame
    hsv = cv2.cvtColor(foto, cv2.COLOR_BGR2HSV)#converto in hsv

    greyRed = cv2.inRange(hsv, lower_red, upper_red)#ottengo la scala di grigi in base al threshold fornito
    #greyBlue = cv2.inRange(hsv, lower_blue, upper_blue)
    #greyGreen = cv2.inRange(hsv, lower_green, upper_green)

    #Applico hough circle transform
    circlesRed = cv2.HoughCircles(greyRed, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=20, maxRadius=200)
    circlesGreen = 0#cv2.HoughCircles(greyGreen, cv2.HOUGH_GRADIENT, 1, 50 ,param1 = 50, param2 = 30, minRadius = 20, maxRadius = 200)
    circlesBlue = 0#cv2.HoughCircles(greyBlue, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=20, maxRadius=200)

    #Gestisco il caso in cui non vi siano cerchi nel frame( assurdo )
    if circlesRed or circlesGreen or circlesBlue is None:
        print("Nessuna circonferenza trovata")
        continue
    #Disegno le circonferenze DEBUG
    circlesRed = np.uint16(np.around(circlesRed))
    for i in circlesRed[0, :]:
        cv2.circle(foto, (i[0], i[1]), i[2], (0, 0, 255), 1)  # draw the outer circle
        cv2.circle(foto, (i[0], i[1]), 2, (0, 0, 255), 3)  # draw the center of the circle
        cv2.imwrite('processed/0processed.png',foto)