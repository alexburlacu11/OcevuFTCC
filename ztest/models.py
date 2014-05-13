from django.db import models





class Request(models.Model):
    name = models.CharField(max_length=100)
    laboratory = models.CharField(max_length=100)
    telnumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100) 
    request_is_ALERT = models.BooleanField()
    sequences_number = models.IntegerField()       
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    status = models.CharField(max_length=100, default='INVALID')
    
    def get_cname(self):
        class_name = "Requests"
        return class_name
 
 
class Sequence(models.Model):
    request = models.ForeignKey(Request)
    coord_system_id = models.CharField(max_length=20)
    target_ra = models.CharField(max_length=20)
    target_dec = models.CharField(max_length=20)    
    jd1 = models.CharField(max_length=20)
    jd2 = models.CharField(max_length=20)
    event_type = models.CharField(max_length=20) 
    burst_id = models.CharField(max_length=20) 
    priority = models.IntegerField()
    duration = models.IntegerField()  
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    status = models.CharField(max_length=100, default='INVALID') 
    
    def get_cname(self):
        class_name = "Sequences"
        return class_name
    
 
class Album(models.Model):
    sequence = models.ForeignKey(Sequence)    
    type = models.CharField(max_length=20) #vis nir other
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    status = models.CharField(max_length=100, default='INVALID')
    
    def get_cname(self):
        class_name = "Albums"
        return class_name
    
         
class Plan(models.Model):
    album = models.ForeignKey(Album)
    iteration_number = models.IntegerField()
    integration_time = models.IntegerField()
    filter = models.CharField(max_length=100) #B,V,R,I
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    status = models.CharField(max_length=100, default='INVALID')
    
    def get_cname(self):
        class_name = "Plans"
        return class_name
    
    