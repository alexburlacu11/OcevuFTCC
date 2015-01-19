# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from alertManager.models import Alert

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    
class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ['ivorn', 'author', 'role']
       
    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['ivorn'].widget.attrs['class'] = "form-control"
        self.fields['role'].widget.attrs['class'] = "form-control"
        self.fields['author'].widget.attrs['class'] = "form-control"
   