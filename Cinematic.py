import serial

ser = serial.Serial('COM8', 9600)

def write(data):
    ser.write(data)
    print('done')
    ser.close()

write()
