from django.db import models
from django.db import models
import copy

from lxml import etree as ET
import datetime
import os
from uuid import uuid4
import sys
import os
import getopt


# Create your models here.
class Request(models.Model):
    name = models.CharField(max_length=100)
    laboratory = models.CharField(max_length=100)
    telnumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    creation_date = models.CharField(max_length=100)  
    request_is_ALERT = models.BooleanField()
    seq_number = models.IntegerField()    
    date = models.DateTimeField(auto_now_add=True, blank=True,)
    

    def get_absolute_url(self):
        return "/routinemanager/view/%i/" % self.id
            
    def get(self, id_):        
        v = RoutineRequest.objects.get(pk=id_)
        return v
    
    def getByID(self, id):
        a = RoutineRequest.objects.filter(pk=id)
        return a

    def getAll(self):        
        v = RoutineRequest.objects.all().order_by('-date')
        return v
        
    def loadRequestFromXML(self, xml_filename):           
        
        with open (xml_filename, "r") as myfile:
            data=myfile.read()
            
#         v = voeparse.loads(data, False)

        r = Request()        
        a = r.format_to_html(xml_filename)
                
        return data 

    def format_to_html(self, xml_filename):
        aa = "not yet implemented"
        return aa

class Sequence(models.Model):       
    request = models.ForeignKey(Request)
    name = models.CharField(max_length=100) 
    
    
  
class Document(models.Model):
        
    docfile = models.FileField(upload_to='documents/')
    
        

   