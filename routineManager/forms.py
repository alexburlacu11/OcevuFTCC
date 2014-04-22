# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import RoutineRequest

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    
class RoutineRequestForm(ModelForm):
    class Meta:
        model = RoutineRequest
       
    def __init__(self, *args, **kwargs):
        super(RoutineRequestForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['laboratory'].widget.attrs['class'] = "form-control"
        self.fields['telnumber'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['creation_date'].widget.attrs['class'] = "form-control"
        self.fields['request_is_ALERT'].widget.attrs['class'] = "form-control"
        self.fields['seq_number'].widget.attrs['class'] = "form-control"

    