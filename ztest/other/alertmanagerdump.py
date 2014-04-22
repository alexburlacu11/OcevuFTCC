from django.db import models
import copy
import voeparse
from lxml import etree as ET
import datetime
        
# Create your models here.


# TODO: voevent class qqs with 

class Alert_Main(models.Model):
    ivorn = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True,)
#     importance = models.FloatField(null=True, blank=True,)
#     expires = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
#     observation_astro_coord_system_id = models.IntegerField(null=True, blank=True,)
#     observation_time = models.DateTimeField('observation_time',null=True, blank=True,)
#     observation_time_unit = models.CharField(max_length=100)
#     observation_time_error = models.DateTimeField('observation_time_error',null=True, blank=True,)
#     position_2d_value_1 = models.FloatField(null=True, blank=True,)
#     position_2d_value_2 = models.FloatField(null=True, blank=True,)
#     position_2d_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_2d_error2radius = models.FloatField(null=True, blank=True,)
#     observatory_id = models.IntegerField(null=True, blank=True,)
#     observatory_astro_coord_system_id = models.IntegerField(null=True, blank=True,)
#     position_3d_value_1 = models.FloatField(null=True, blank=True,)
#     position_3d_value_2 = models.FloatField(null=True, blank=True,)
#     position_3d_value_3 = models.FloatField(null=True, blank=True,)
#     position_3d_value1_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_3d_value2_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_3d_value3_unit = models.CharField(max_length=20,null=True, blank=True,)
    
    def __unicode__(self):
        return u"%s %s" % (self.ivorn, self.author)
    
    def now_plus_30(): 
        return auto_now_add + timedelta(days = 30)
     
 
class Alert_Concepts(models.Model):
    concept_name = models.CharField(max_length=100,null=True, blank=True,)
#     description = models.CharField(max_length=200,null=True, blank=True,)
#     name = models.CharField(max_length=100,null=True, blank=True,)
#     inference_probability = models.FloatField(null=True, blank=True,)
#     inference_relation = models.CharField(max_length=100,null=True, blank=True,)
#     #many to many with main 
#     alerts = models.ManyToManyField(Alert_Main)


class Alert_Instruments(models.Model):
    description = models.CharField(max_length=200,null=True, blank=True,)
#     reference = models.CharField(max_length=200,null=True, blank=True,)
#     #many to many with main 
#     alerts = models.ManyToManyField(Alert_Main)
    

class Alert_Citations(models.Model):
    IVO = models.CharField(max_length=200,null=True, blank=True,)
#     event_ivo_cite = models.CharField(max_length=200,null=True, blank=True,)
#     description = models.CharField(max_length=200,null=True, blank=True,)
#     #pk to main id
#    Alert_Mainid = models.ForeignKey(Alert_Main,null=True, blank=True,)
    
    
class Alert_Parameters(models.Model):
    param_name = models.CharField(max_length=200,null=True, blank=True,)
#     value = models.FloatField(null=True, blank=True,)
#     unit = models.CharField(max_length=20,null=True, blank=True,)
#     ucd = models.CharField(max_length=20,null=True, blank=True,)
#     data_type = models.CharField(max_length=20,null=True, blank=True,)
#     u_type = models.CharField(max_length=20,null=True, blank=True,)
#     description = models.CharField(max_length=200,null=True, blank=True,)
#     reference = models.CharField(max_length=200,null=True, blank=True,)
#     group_name = models.CharField(max_length=200,null=True, blank=True,)
#     group_description = models.CharField(max_length=200,null=True, blank=True,)
#     group_type = models.CharField(max_length=200,null=True, blank=True,)
#     table_flag = models.BooleanField(blank=True,)
#     #pk to main id
#    Alert_Mainid = models.ForeignKey(Alert_Main,null=True, blank=True,) 
    
class Alert_Parameters_Tables(models.Model):
    table_description = models.CharField(max_length=200,null=True, blank=True,)
#     field_name = models.CharField(max_length=20,null=True, blank=True,)
#     unit = models.CharField(max_length=20,null=True, blank=True,)
#     ucd = models.CharField(max_length=20,null=True, blank=True,)
#     data_type = models.CharField(max_length=200,null=True, blank=True,)
#     values = models.IntegerField(null=True, blank=True,)
#     #pk to main id
#     Alert_Mainid = models.ForeignKey(Alert_Main, null=True, blank=True,)
    
class VOEvent:
    main = Alert_Main()
  
#     concepts = Alert_Concepts()
#     instruments = Alert_Instruments()
#     citations = Alert_Citations()
#     parameters = Alert_Parameters()
#     parameters_tables = Alert_Parameters_Tables()
    
    def saveVOEvent(self):
        self.main.save()
#         self.concepts.save()
#         self.instruments.save()
#         self.citations.save()
#         self.parameters.save()
#         self.parameters_tables.save()
        
    def getVOEvent(self, id):        
        v = VOEvent() 
        v.main = Alert_Main.objects.filter(pk=id)
#         v.concepts = Alert_Concepts.objects.filter(pk=id)
#         v.instruments = Alert_Instruments.objects.filter(pk=id)
#         v.citations = Alert_Citations.objects.filter(pk=id)
#         v.parameters = Alert_Parameters.objects.filter(pk=id)
#         v.parameters_tables = Alert_Parameters_Tables.objects.filter(pk=id)
        return v
    
    def showIVORN(self):
        return self.main.ivorn
    
    def loadFromXML(self, xml_filename):           
        
        with open (xml_filename, "r") as myfile:
            data=myfile.read()
            
        v = voeparse.loads(data, False)
        
        
        my_event = VOEvent() 
        main = Alert_Main(ivorn=v.attrib['ivorn'])
        main.save()
        my_event.main = main
#         my_event.concepts = Alert_Concepts(concept_name="my concept",Alert_Mainid_id=1,)
#         my_event.instruments = Alert_Instruments(description="infrared instrument",Alert_Mainid=1,)
#         my_event.citations = Alert_Citations(IVO="citations ivo",Alert_Mainid=1,)
#         my_event.parameters = Alert_Parameters(param_name="some param",Alert_Mainid=1,)
#         my_event.parameters_tables = Alert_Parameters_Tables(table_description="table description",Alert_Mainid=1,)
#        my_event.saveVOEvent()
        
        return my_event
        
        
    
    
    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')
    

   