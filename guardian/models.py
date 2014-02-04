from django.db import models
import datetime
import serial


class Watcher(models.Model):
    date = models.DateTimeField('time');
    sensor_value = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    class Meta:
        abstract = True
        
    def set_date(self, date):
        self.date = date    
        
    def set_port(self, port):
        self.port = port
        
    def read_serial(self):
        try:
           self.sensor_value = serial.Serial(self.port, 9600).readline()
        except ValueError:
           print "Error in reading from serial \n"        
           self.sensor_value = 0
           
    def to_string(self):
        print "Last value of watcher: \n"

class WeatherWatcher(Watcher):
    def to_string(self):       
        print "Last value of weather station: \n" + str(self.sensor_value)
        
class SiteWatcher(Watcher):
    def to_string(self):
        print "Last value of site sensor: \n" + str(self.sensor_value)
        
class SecurityWatcher(Watcher):
    def to_string(self):
        print "Last value of security sensor: \n" + str(self.sensor_value) 


               
 
class Agent(models.Model):
    class Meta:
        abstract = True
        
 
    def log(self):
        pass
    

    def to_string(self):
        pass


       
class Guardian(Agent):
    date = models.DateTimeField('time')
    weather_flag = models.BooleanField("weather")
    site_flag = models.BooleanField("site")
    security_flag = models.BooleanField("security")
    
    def set_date(self, date):
        self.date = date
    
    def set_weather(self, status):
        weather_flag = status
        
    def set_site(self, status):
        site_flag = status
        
    def set_security(self, status):
        security_flag = status   
        
    def log(self): 
        #TO DO: insert in database log function for the Guardian agent
        raise Exception("TODO: Function not yet implemented")
        
    def to_string(self):
        if (self.weather_flag == True):
            print "Weather status is GOOD ! \n"    
        else:
            print "Weather status is BAD ! \n"  
        
        if (self.site_flag == True):
            print "Site status is GOOD ! \n"    
        else:
            print "Site status is BAD ! \n"  
            
        if (self.weather_flag == True):
            print "Security status is GOOD ! \n"    
        else:
            print "Security status is BAD ! \n"  

