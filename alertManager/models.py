from django.db import models

# Create your models here.

class Alert_Main(models.Model):
    ivorn = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateTimeField('date')
    importance = models.models.FloatField
    expires = models.DateTimeField('expires')
    observation_astro_coord_system_id = models.IntegerField
    observation_time = models.DateTimeField('observation_time')
    observation_time_unit = models.CharField(max_length=100)
    observation_time_error = models.DateTimeField('observation_time_error')
    position_2d_value_1 = models.FloatField
    position_2d_value_2 = models.FloatField
    position_2d_unit = models.CharField(max_length=20)
    position_2d_error2radius = models.FloatField
    observatory_id = models.IntegerField    
    observatory_astro_coord_system_id = models.IntegerField
    position_3d_value_1 = models.FloatField
    position_3d_value_2 = models.FloatField
    position_3d_value_3 = models.FloatField
    position_3d_value1_unit = models.CharField(max_length=20)
    position_3d_value2_unit = models.CharField(max_length=20)
    position_3d_value3_unit = models.CharField(max_length=20)
     
 
class Alert_Concepts(models.Model):
    concept_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    inference_probability = models.FloatField
    inference_relation = models.CharField(max_length=100)
    #many to many with main 
    alerts = models.ManyToManyField(Alert_Main)


class Alert_Instruments(models.Model):
    description = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
    #many to many with main 
    alerts = models.ManyToManyField(Alert_Main)
    

class Alert_Citations(models.Model):
    IVO = models.CharField(max_length=200)
    event_ivo_cite = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #pk to main id
    Alert_Mainid = models.ForeignKey(Alert_Main)
    
    
class Alert_Parameters(models.Model):
    param_name = models.CharField(max_length=200)
    value = models.FloatField
    unit = models.CharField(max_length=20)
    ucd = models.CharField(max_length=20)
    data_type = models.CharField(max_length=20)
    u_type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
    group_name = models.CharField(max_length=200)
    group_description = models.CharField(max_length=200)
    group_type = models.CharField(max_length=200)
    table_flag = models.BooleanField
    #pk to main id
    Alert_Mainid = models.ForeignKey(Alert_Main) 
    
class Alert_Parameters_Tables(models.Model):
    table_description = models.CharField(max_length=200)
    field_name = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    ucd = models.CharField(max_length=20)
    data_type = models.CharField(max_length=200)
    values = models.IntegerField
    #pk to main id
    Alert_Mainid = models.ForeignKey(Alert_Main)

   