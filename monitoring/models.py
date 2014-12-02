from django.db import models
from common.models import Agent, Sender
import socket
import time
from random import randint
from threading import Thread
import math



class MonitoringSender(Sender):   
    
    def run(self):
        print "Monitoring Sender started"
        while True:
            """send data to others if value is outside min max or difference is higher than delta"""          
            darkness = ConditionsStatus.objects.filter(parameterName="Darkness").first()
            if (math.fabs(float(darkness.parameterCurrentValue) - float(darkness.parameterPreviousValue) >= float(darkness.parameterDelta)) or darkness.parameterCurrentValue < darkness.parameterMin or darkness.parameterCurrentValue > darkness.parameterMax):
                
                self.notifyObservers("Darkness:"+str(darkness.parameterCurrentValue))
                                  
            time.sleep(4)
                
            """send all parameters in socket instead of each separately"""

class MonitoringController(Agent):
    
    def __init__(self):
        Agent.__init__(self, 'Monitoring')
        self.sender = MonitoringSender(self.agentName+"Sender", self.ip, self.receivePort, self.sendBufferSize)
        self.weather = WeatherWatcher()
        self.conditions = ConditionsWatcher()
        self.watchers = [self.weather, self.conditions ]#SecurityWatcher, SiteWatcher ]

    def work(self):
        weather = WeatherStatus()
        weather.initParameters()
        conditions = ConditionsStatus()
        conditions.initParameters()
        
        for watcher in self.watchers:
            watcher.start()
            time.sleep(1)
              
        
      
    def analyseMessage(self, conn , data):        
        dataSet = data.split(":")
        rtype = dataSet[0]
        ip = dataSet[1]
        port = dataSet[2]
        if rtype == "register":
            obs = [o for o in self.sender.observers if o == ip+":"+str(port)]
            if len(obs) == 0:
                print "New client registered"
                self.addObserver(ip+":"+str(port))
                conn.send("ok\n")
            else:
                print "Client already registered"
                conn.send("Already registered\n")

class Status(models.Model):
    parameterName = models.CharField(max_length=20)
    parameterCurrentValue = models.CharField(max_length=20)
    parameterPreviousValue = models.CharField(max_length=20)
    parameterUnit = models.CharField(max_length=20)
    parameterMin = models.CharField(max_length=20)
    parameterMax = models.CharField(max_length=20)
    parameterDelta = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
    def initParameters(self):
        """initialise parameters"""

class WeatherStatus(Status):
    def initParameters(self):
        WeatherStatus.objects.all().delete()
        rain = WeatherStatus(parameterName="Rain", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit = "mm", parameterMin="20", parameterMax="60", parameterDelta="10")
        rain.save()
        fog = WeatherStatus(parameterName="Fog", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit = "mm", parameterMin="20", parameterMax="60", parameterDelta="10")
        fog.save()
        wind = WeatherStatus(parameterName="Wind", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit = "km/h", parameterMin="20", parameterMax="60", parameterDelta="10")
        wind.save()

class ConditionsStatus(Status):        
    def initParameters(self):
        ConditionsStatus.objects.all().delete()
        clouds = ConditionsStatus(parameterName="Clouds", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit="%", parameterMin="20", parameterMax="60", parameterDelta="10")
        clouds.save()
        transparency = ConditionsStatus(parameterName="Transparency", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit="%", parameterMin="20", parameterMax="60", parameterDelta="10")
        transparency.save()
        seeing = ConditionsStatus(parameterName="Seeing", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit="%", parameterMin="20", parameterMax="60", parameterDelta="10")
        seeing.save()
        darkness = ConditionsStatus(parameterName="Darkness", parameterCurrentValue="20", parameterPreviousValue="20", parameterUnit="%", parameterMin="20", parameterMax="60", parameterDelta="10")
        darkness.save()
        
        
        
class Watcher(Thread):
    
    class Meta:
        abstract = True
        
    def getValueFromSensor(self, port):
        """get value from sensor on port port"""
        return randint(port-30,port)


class WeatherWatcher(Watcher):
    """gets information from all weather sensors and inputs them in the db"""
    def run(self):
        while True:            
            rain = WeatherStatus.objects.filter(parameterName="Rain").first()
            rain.parameterPreviousValue = rain.parameterCurrentValue
            rain.parameterCurrentValue = self.getValueFromSensor(60)
            rain.save()
            print "Rain: "+ str(rain.parameterCurrentValue)
            time.sleep(4)
            
            
class ConditionsWatcher(Watcher):
    """gets information such as cloud, transparency, seeing, darkness"""
    def run(self):
        while True:            
            darkness = ConditionsStatus.objects.filter(parameterName="Darkness").first() 
            darkness.parameterPreviousValue = darkness.parameterCurrentValue           
            darkness.parameterCurrentValue = self.getValueFromSensor(60)
            darkness.save()
            print "Darkness: "+ str(darkness.parameterCurrentValue)
            time.sleep(4)
            
    
    
# class SiteStatus(Status):
# 
# class SiteWatcher(Agent):
#     
# class SecurityStatus(Status):
# 
# class SecurityWatcher(Agent):
        


