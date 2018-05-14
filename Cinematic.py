import serial

ser = serial.Serial('COM3', 9600)
connected = False
def connect():
    c = ser.read()
    if(c=='C'):
        connected = True
        print('connected')
    return connected

def write(data):
    if(connect()):
        ser.write(data)
        print('done')
        ser.close()

write(300)