from django.db import models
from django.template.defaultfilters import length

# Create your models here.


class Request(models.Model):
    name = models.CharField(max_length=20)
    laboratory = models.CharField(max_length=20)
    telnumber = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    target_type = models.CharField(max_length=20, default='IMMEDIATE') 
#     request_is_ALERT = models.BooleanField()
#     sequences_number = models.IntegerField()       
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('SUBMITTED', 'SUBMITTED'),
    ('PLANNED', 'PLANNED'),
    ('REJECTED', 'REJECTED'),
    ('EXECUTING', 'EXECUTING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=20, default='INCOMPLETE',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Requests"
        return class_name
 
 
class Sequence(models.Model):
    request = models.ForeignKey(Request)
    name = models.CharField(max_length=20)
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
    coord_system_id = models.CharField(max_length=20, choices=TYPE_COORD_SYSTEM, default='UTC-FK5-TOPO')
    target_ra_dec = models.CharField(max_length=20)      
    jd1 = models.CharField(max_length=20)
    jd2 = models.CharField(max_length=20)  
    duration = models.IntegerField(default=0)     
    TYPE_EVENT = (
    ('Rapid_Alert_burst', 'Rapid_Alert_burst'),
    ('Full_Alert_burst', 'Full_Alert_burst'),
    ('Rapid_Routine', 'Rapid_Routine'),
    ('Full_routine', 'Full_routine'),    
    )   
    event_type = models.CharField(max_length=20, choices=TYPE_EVENT) 
    INTERNAL_PRIORITY = (
    ('0', '0'),
    ('1', '1'),    
    )   
    priority = models.CharField(max_length=1, choices=INTERNAL_PRIORITY, default='0')    
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('SUBMITTED', 'SUBMITTED'),
    ('PLANNED', 'PLANNED'),
    ('REJECTED', 'REJECTED'),
    ('EXECUTING', 'EXECUTING'),   
    ('DONE', 'DONE'), 
    )
    status = models.CharField(max_length=20, default='INCOMPLETE',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Sequences"
        return class_name
    
 
class Album(models.Model):
    sequence = models.ForeignKey(Sequence)
    TYPE_ALBUM = (
    ('VISIBLE', 'ALBUM_VIS'),
    ('INFRARED', 'ALBUM_NIR'),
    ('SPECTRO', 'ALBUM_SPEC'),    
    )        
    type = models.CharField(max_length=10, choices=TYPE_ALBUM) #vis nir other
#     plans_number = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)    
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),    
    ('COMPLETE', 'COMPLETE'), 
    )
    status = models.CharField(max_length=20, default='INCOMPLETE',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Albums"
        return class_name
    
         
class Plan(models.Model):
    album = models.ForeignKey(Album)
    iteration_number = models.IntegerField()
    integration_time = models.IntegerField()
    wavelength = models.CharField(max_length=20)
    TYPE_FILTER = (
    ('Filter_B', 'Filter_B'),
    ('Filter_V', 'Filter_V'),
    ('Filter_R', 'Filter_R'),   
    ('Filter_I', 'Filter_I'), 
    )  
    filter = models.CharField(max_length=10, choices=TYPE_FILTER) #B,V,R,I
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),    
    ('COMPLETE', 'COMPLETE'), 
    )
    status = models.CharField(max_length=20, default='INCOMPLETE',choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Plans"
        return class_name
    
    
class SummaryManager(): 
     
    @staticmethod   
    def get_summary(request_id):
        
#         global_summary = ( {
#                             "name_of_sequence1" : 
#                             ( 
#                              { "album11":("plan111","plan112") },
#                              { "album12":("plan121","plan122") } 
#                             )
#                          },
#                           {
#                             "name_of_sequence2" : 
#                             ( 
#                              { "album21":("plan211","plan212") },
#                              { "album22":("plan221","plan222") } 
#                             )
#                           }               
#                            
#                            ) 
         
        request_object = Request.objects.get(id=request_id)
        sequences = Sequence.objects.all()
        
        global_summary = "Nothing"
        global_summary = {}
        
        for seq in sequences:
            
            for alb in Album.objects.filter(sequence=seq):
                
                global_summary = ( { seq.name : ( { alb : Plan.objects.filter(album=alb)} ) } )
             
        
        if length(global_summary) == 0:
            global_summary = "Nothing"
        
#         x = {}
# 
#         for row in sequences:
#            x[row.name] = {} # derive this from something.
#            for idx, col in enumerate(row):
#                x[row.name][idx] = col
       
       
        return global_summary
    
    
    
    
#     <ul>
#                                 {% for sequence in global_summary %} 
#                                   
#                                        {% for name_of_seq, list_of_albums in sequence.items %} 
#                                        
#                                       <p>{{name_of_seq}}</p>
#                                       
#                                           {% for album in list_of_albums %}     
#                                                                                 
#                                               {% for name_of_album, list_of_plans in album.items %} 
#                                               
#                                               <p>{{name_of_album}}</p>
#                                               
#                                                   {% for plan in list_of_plans %} 
#                                                   
#                                                   <p>{{plan}}</p>
#                                                       
#                                                                                 
#                                                  {% endfor %}    
#                                                                             
#                                              {% endfor %}    
#                                                                         
#                                          {% endfor %}    
#                                                                     
#                                      {% endfor %}                          
#                                  {% endfor %}
#                             </ul>
#                             
#                             <hr>
    
    