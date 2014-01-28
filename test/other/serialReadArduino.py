import serial

ser1 = serial.Serial('/dev/ttyACM0',9600)
ser2 = serial.Serial('/dev/ttyACM1',9600)

rain = ser1.readline()
distance = ser2.readline()

while(True):    
    rain = ser1.readline()
    distance = ser2.readline()
    if (float(rain) > 1000):
        print "it's raining !"
        print "\n"
    if (float(distance) < 10): 
        print "security !"
        print "\n"
    ser1.flush()
    ser2.flush()