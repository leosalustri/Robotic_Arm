import cv2
import numpy as np
import math

#Inizializza la capture video
cap = cv2.VideoCapture(0)

#Parametri hsv da cercare
lower_red = np.array([140,50,0])#da controllare i valori con le dovute proporzioni.
upper_red = np.array([140,50,0])

lower_blue = np.array([104,120,45])#da controllare i valori con le dovute proporzioni.
upper_blue = np.array([124,255,150])

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
    greyBlue = cv2.inRange(hsv, lower_blue, upper_blue)
    greyGreen = cv2.inRange(hsv, lower_green, upper_green)

    #Applico hough circle transform settare i parametri in base alle conversioni cm in pixel del sistema di riferimento.
    circlesRed = cv2.HoughCircles(greyRed, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=20, maxRadius=200)
    circlesGreen = cv2.HoughCircles(greyGreen, cv2.HOUGH_GRADIENT, 1, 50 ,param1 = 50, param2 = 30, minRadius = 20, maxRadius = 200)
    circlesBlue = cv2.HoughCircles(greyBlue, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=10, maxRadius=1000)

    #Gestisco il caso in cui non vi siano cerchi nel frame( assurdo )
    if circlesRed or circlesGreen or circlesBlue is None:
        print("Nessuna circonferenza trovata")
        continue
    #Disegno le circonferenze DEBUG
    circlesBlue = np.uint16(np.around(circlesBlue))
    for i in circlesBlue[0, :]:
        cv2.circle(foto, (i[0], i[1]), i[2], (255, 0, 0), 1)  # draw the outer circle
        cv2.circle(foto, (i[0], i[1]), 2, (255, 0, 0), 3)  # draw the center of the circle
        cv2.imwrite('processed/0processed.png',foto)





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


#import Cinematic
#Cinematic.write(220)