from django import forms

from models import Request
from models import Sequence
from models import Album
from models import Plan


from django.forms import ModelForm
from django.forms.models import inlineformset_factory



class RequestForm(ModelForm):
    class Meta:
        model = Request

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['laboratory'].widget.attrs['class'] = "form-control"
        self.fields['telnumber'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"        
        self.fields['request_is_ALERT'].widget.attrs['class'] = "form-control"
        self.fields['target_type'].widget.attrs['class'] = "form-control"
        self.fields['sequences_number'].widget.attrs['class'] = "form-control"
        
SequenceFormSet = inlineformset_factory(Request, Sequence, extra=1)
AlbumFormSet = inlineformset_factory(Sequence, Album, extra=1)
PlanFormSet = inlineformset_factory(Album, Plan, extra=1)


