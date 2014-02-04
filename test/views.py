from django.shortcuts import render
from models import *

def test(self):
    print "polymorphism test: \n"
    w = WeatherWatcher(
         port='/dev/ttyACM0', 
         date=datetime.date.today(), 
         sensor_value=0
    )
    s = SiteWatcher(
         port='/dev/ttyACM1', 
         date=datetime.date.today(), 
         sensor_value=0
    )  
    ww = Watcher(
         port='/dev/ttyACM0', 
         date=datetime.date.today(), 
         sensor_value=0
    )
    watchers = [ww, w,s]        
    
    for q in watchers:
        q.read_serial()
        q.save()
        
    for q in watchers:
        print "watcher says: \n"
        print q.to_string() 