# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import Request
from models import Sequence

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    
class RequestForm(ModelForm):
    class Meta:
        model = Request
       
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['laboratory'].widget.attrs['class'] = "form-control"
        self.fields['telnumber'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['creation_date'].widget.attrs['class'] = "form-control"
        self.fields['request_is_ALERT'].widget.attrs['class'] = "form-control"
        self.fields['seq_number'].widget.attrs['class'] = "form-control"
        
class SequenceForm(ModelForm):
    class Meta:
        model = Sequence
       
    def __init__(self, *args, **kwargs):
        super(SequenceForm, self).__init__(*args, **kwargs)
        self.fields['request'].widget.attrs['class'] = "form-control"
        self.fields['name'].widget.attrs['class'] = "form-control"
        

    