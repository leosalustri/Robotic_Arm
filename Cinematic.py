import time
import serial
ser = serial.Serial('COM7',9600)

time.sleep(3)
ser.write(220)
print('done')
ser.close()