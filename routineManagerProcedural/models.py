from django.db import models
from django.template.defaultfilters import length

# Create your models here.


class Request(models.Model):
    name = models.CharField(max_length=20)
    laboratory = models.CharField(max_length=20)
    telnumber = models.CharField(max_length=20)
    email = models.CharField(max_length=75)
    TYPE_TARGET = (
    ('GAMMA_BURST', 'GAMMA_BURST'),
    ('METEOR_SHOWER', 'METEOR_SHOWER'),  
    ('SOLAR_EVENT', 'SOLAR_EVENT'),
    ('COMET', 'COMET'),  
    ('CELESTIAL_EVENT', 'CELESTIAL_EVENT'),  
    ('UNKNOWN', 'UNKNOWN'),   
    )
    target_type = models.CharField(max_length=20, default='GAMMA_BURST', choices=TYPE_TARGET) 
    julian_day_start = models.CharField(max_length=20)
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
    TYPE_EXEC_NIGHT = (
    ('Tonight', 'Tonight'),                   
    ('J+1', 'J+1'),
    ('J+2', 'J+2'),
    ('J+3', 'J+3'),
    ('J+4', 'J+4'),
    ('J+5', 'J+5'),
    ('J+6', 'J+6'),
    ('J+7', 'J+7'),
    ('J+8', 'J+8'),
    ('J+9', 'J+9'),
    )
    executing_night = models.CharField(max_length=20, choices=TYPE_EXEC_NIGHT, default='Tonight')
    julian_day_1 = models.CharField(max_length=20)
    julian_day_2 = models.CharField(max_length=20)  
    TYPE_EXPOSURE_PREFERENCE = (
    ('IMMEDIATE', 'IMMEDIATE'),
    ('BEST_ELEVATION', 'BEST_ELEVATION'),
    ('BETWEEN_JD1_JD2', 'BETWEEN_JD1_JD2'),    
    )
    start_exposure_preference = models.CharField(max_length=20, choices=TYPE_EXPOSURE_PREFERENCE, default='IMMEDIATE')
    duration = models.IntegerField(default=0)      
    has_priority = models.BooleanField(default=False)
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
    duration = models.IntegerField(default=0)     
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)   
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('COMPLETE', 'COMPLETE'),
    )
    status = models.CharField(max_length=10, default='INCOMPLETE', choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Albums"
        return class_name
    
         
class Plan(models.Model):
    album = models.ForeignKey(Album)
    iterations_number = models.IntegerField()
    exposure_time = models.IntegerField()    
    TYPE_FILTER = (
    ('Filter_B', 'Filter_B'),
    ('Filter_V', 'Filter_V'),
    ('Filter_R', 'Filter_R'),   
    ('Filter_I', 'Filter_I'), 
    )  
    filter = models.CharField(max_length=10, choices=TYPE_FILTER) #B,V,R,I
    wavelength = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True,)    
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('COMPLETE', 'COMPLETE'),
    )
    status = models.CharField(max_length=10, default='INCOMPLETE', choices=TYPE_STATUS)
    
    def get_cname(self):
        class_name = "Plans"
        return class_name
    
"""@TODO:"""
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
        sequences = Sequence.objects.filter(request=request_object)
        
        
        global_summary = []
        aux = []
#         message = ('Void',)
#         for seq in sequences:
#             
#             for alb in Album.objects.filter(sequence=seq):
#                 
#                 global_summary = ( { seq.name : ( { alb : Plan.objects.filter(album=alb)} ) } )

        if length(sequences) != 0:
            for seq in sequences:
                albums = Album.objects.filter(sequence=seq)
                for album in albums:
                    plans = Plan.objects.filter(album=album)
                    aux.append( {album : plans} )
                global_summary.append({ seq : aux } )
       
        
#         x = {}
# 
#         for row in sequences:
#            x[row.name] = {} # derive this from something.
#            for idx, col in enumerate(row):
#                x[row.name][idx] = col
       
#         print global_summary[0].itervalues()
       
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
    
    