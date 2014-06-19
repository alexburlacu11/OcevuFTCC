
from models import Request
from models import Sequence
from models import Album
from models import Plan


from django.forms import ModelForm
from django import forms
from django.db.models.base import Empty
from django.core.validators import EMPTY_VALUES



class RequestForm(ModelForm):
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('SUBMITTED', 'SUBMITTED'),
    ('PLANNED', 'PLANNED'),
    ('REJECTED', 'REJECTED'),
    ('EXECUTING', 'EXECUTING'),    
    ('DONE', 'DONE'), 
    )
   
    status = forms.CharField()
    
    class Meta: 
        model = Request
        
 
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs['class'] = "form-control"
#         self.fields['laboratory'].widget.attrs['class'] = "form-control"        
#         self.fields['telnumber'].widget.attrs['class'] = "form-control"
#         self.fields['email'].widget.attrs['class'] = "form-control"     
        self.fields['laboratory'].widget.attrs['readonly'] = True        
        self.fields['telnumber'].widget.attrs['readonly'] = True 
        self.fields['email'].widget.attrs['readonly'] = True 
#         self.fields['request_is_ALERT'].widget.attrs['class'] = "form-control"
#         self.fields['target_type'].widget.attrs['class'] = "form-control"
#         self.fields['sequences_number'].widget.attrs['class'] = "form-control"
#         self.fields['sequences_number'].widget.attrs['readonly'] = True
#         self.fields['status'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['readonly'] = True
        
         
 
class SequenceForm(ModelForm):
    TYPE_STATUS = (
    ('INCOMPLETE', 'INCOMPLETE'),
    ('SUBMITTED', 'SUBMITTED'),
    ('PLANNED', 'PLANNED'),
    ('REJECTED', 'REJECTED'),
    ('EXECUTING', 'EXECUTING'),    
    ('DONE', 'DONE'), 
    )
    
    ra_dec_example = (
    ('20 54 05.689 +37 01 17.38', '20 54 05.689 +37 01 17.38'),
    ('10:12:45.3-45:17:50', '10:12:45.3-45:17:50'),
    ('350.123456 -17.33333', '350.123456 -17.33333'),
    )
    format_ra_dec = forms.ChoiceField(choices=ra_dec_example) 
    
    status = forms.CharField()
    
    class Meta:
        model = Sequence
        exclude = ('request',)
 
    def __init__(self, *args, **kwargs):
        super(SequenceForm, self).__init__(*args, **kwargs)        
#         self.fields['request'].widget.attrs['class'] = "form-control"
#         self.fields['request'].widget.attrs['readonly'] = True
#         self.fields['name'].widget.attrs['class'] = "form-control"
#         self.fields['coord_system_id'].widget.attrs['class'] = "form-control"
#         self.fields['executing_night'].widget.attrs['class'] = "form-control"   
#         self.fields['target_ra_dec'].widget.attrs['class'] = "form-control"                
#         self.fields['jd1'].widget.attrs['class'] = "form-control"
#         self.fields['jd2'].widget.attrs['class'] = "form-control"
#         self.fields['duration'].widget.attrs['class'] = "form-control"
#         self.fields['priority'].widget.attrs['class'] = "form-control"
# #         self.fields['event_type'].widget.attrs['class'] = "form-control"        
#         self.fields['start_exposure_preference'].widget.attrs['class'] = "form-control"        
#         self.fields['status'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['duration'].widget.attrs['readonly'] = True
        

class AlbumForm(ModelForm):
    
    status = forms.CharField()
    
    class Meta:
        model = Album      
        exclude = ('sequence',)  
 
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
#         self.fields['sequence'].widget.attrs['class'] = "form-control"
#         self.fields['sequence'].widget.attrs['readonly'] = True
#         self.fields['type'].widget.attrs['class'] = "form-control"
#         self.fields['plans_number'].widget.attrs['class'] = "form-control"
#         self.fields['status'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['readonly'] = True
#         self.fields['duration'].widget.attrs['class'] = "form-control"
        self.fields['duration'].widget.attrs['readonly'] = True
                 
 
class PlanForm(ModelForm):
    
    status = forms.CharField()
    
    class Meta:
        model = Plan   
        exclude = ('album',)     
         
    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
#         self.fields['album'].widget.attrs['class'] = "form-control"
#         self.fields['album'].widget.attrs['readonly'] = True
#         self.fields['iterations_number'].widget.attrs['class'] = "form-control"
#         self.fields['integration_time'].widget.attrs['class'] = "form-control"
#         self.fields['wavelength'].widget.attrs['class'] = "form-control"
#         self.fields['filter'].widget.attrs['class'] = "form-control"
#         self.fields['status'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['readonly'] = True
        self.fields['duration'].widget.attrs['readonly'] = True
       
    
      
