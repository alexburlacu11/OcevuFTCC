from django.shortcuts import render
from django.http import HttpResponse

import serial
# Create your views here.

def status(request):
    ser = serial.Serial('/dev/ttyACM0',9600)
    a = ser.readline()
    print a
    return HttpResponse("Guardian sensor values: <br> \
        sensor values: " + a)