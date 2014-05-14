from django.db import models

# Create your models here.


class Request(models.Model):
    name = models.CharField(max_length=100)
    laboratory = models.CharField(max_length=100)
    telnumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    target_type = models.CharField(max_length=100) 
#     request_is_ALERT = models.BooleanField()
    sequences_number = models.IntegerField()       
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INVALID', 'INVALID'),
    ('VALID', 'VALID'),
    ('PENDING', 'PENDING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=100, default='INVALID',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Requests"
        return class_name
 
 
class Sequence(models.Model):
    request = models.ForeignKey(Request)
    TYPE_COORD_SYSTEM = (
    ('TT-ICRS-TOPO', 'TT-ICRS-TOPO'),
    ('TT-FK5-TOPO', 'TT-FK5-TOPO'),
    ('UTC-FK5-TOPO', 'UTC-FK5-TOPO'),
    ('GPS-ICRS-TOPO', 'GPS-ICRS-TOPO'),
    ('GPS-FK5-TOPO', 'GPS-FK5-TOPO'),
    ('TT-ICRS-GEO', 'TT-ICRS-GEO'),
    ('UTC-ICRS-GEO', 'UTC-ICRS-GEO'),
    ('TT-FK5-GEO', 'TT-FK5-GEO'),
    ('UTC-FK5-GEO', 'UTC-FK5-GEO'),
    ('GPS-ICRS-GEO', 'GPS-ICRS-GEO'),
    ('TDB-ICRS-BARY', 'TDB-ICRS-BARY'),
    ('TDB-FK5-BARY', 'TDB-FK5-BARY'),
    ('UTC-GEOD-TOPO', 'UTC-GEOD-TOPO'),
    )
    coord_system_id = models.CharField(max_length=20, choices=TYPE_COORD_SYSTEM)
    target_ra = models.CharField(max_length=20)
    target_dec = models.CharField(max_length=20)    
    jd1 = models.CharField(max_length=20)
    jd2 = models.CharField(max_length=20)  
    event_type = models.CharField(max_length=20) 
    TYPE_BURST = (
    ('Rapid_Alert_burst', 'Rapid_Alert_burst'),
    ('Full_Alert_burst', 'Full_Alert_burst'),
    ('Rapid_Routine', 'Rapid_Routine'),
    ('Full_routine', 'Full_routine'),    
    )   
    burst_id = models.CharField(max_length=20, choices=TYPE_BURST) 
    priority = models.IntegerField()
    duration = models.IntegerField()  
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INVALID', 'INVALID'),
    ('VALID', 'VALID'),
    ('PENDING', 'PENDING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=100, default='INVALID',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Sequences"
        return class_name
    
 
class Album(models.Model):
    sequence = models.ForeignKey(Sequence)
    TYPE_ALBUM = (
    ('ALBUM_VIS', 'ALBUM_VIS'),
    ('ALBUM_NIR', 'ALBUM_NIR'),
    ('ALBUM_SPEC', 'ALBUM_SPEC'),    
    )        
    type = models.CharField(max_length=10, choices=TYPE_ALBUM) #vis nir other
    plans_number = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)    
    TYPE_STATUS = (
    ('INVALID', 'INVALID'),
    ('VALID', 'VALID'),
    ('PENDING', 'PENDING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=100, default='INVALID',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Albums"
        return class_name
    
         
class Plan(models.Model):
    album = models.ForeignKey(Album)
    iteration_number = models.IntegerField()
    integration_time = models.IntegerField()
    TYPE_FILTER = (
    ('B', 'B'),
    ('V', 'V'),
    ('R', 'R'),   
    ('I', 'I'), 
    )  
    filter = models.CharField(max_length=10, choices=TYPE_FILTER) #B,V,R,I
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INVALID', 'INVALID'),
    ('VALID', 'VALID'),
    ('PENDING', 'PENDING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=100, default='INVALID',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Plans"
        return class_name