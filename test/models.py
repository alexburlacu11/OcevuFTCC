from django.db import models
import datetime
import serial

# Create your models here.
# class Bla(models.Model):
#     question = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
# 
#     def __unicode__(self):
#         return self.question
# 
#     def was_published_today(self):
#         return self.pub_date.date() == datetime.date.today()
# 
# 
# 
# class Choice(models.Model):
#     poll = models.ForeignKey(Bla)
#     choice = models.CharField(max_length=200)
#     votes = models.IntegerField()
# 
#     def __unicode__(self):
#         return self.choice # this is line 22

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
        serial_port = serial.Serial(self.port,9600)
        self.sensor_value = serial_port.readline()
        
    def to_string(self):
        print "Last value of watcher: \n"






class WeatherWatcher(Watcher):
    def to_string(self):       
        print "Last value of rain sensor: \n" + str(self.sensor_value)
        
class SiteWatcher(Watcher):
    def to_string(self):
        print "Last value of distance sensor: \n" + str(self.sensor_value)
        
        