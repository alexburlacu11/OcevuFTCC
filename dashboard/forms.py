# -*- coding: utf-8 -*-
# from django import forms
# from django.forms import ModelForm
# from models import User

    
# class LoginForm(ModelForm):
#     class Meta:
#         model = User
#        
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['class'] = "form-control"
#         self.fields['password'].widget.attrs['class'] = "form-control"
#         
# class RegistrationForm(ModelForm):
#     class Meta:
#         model = User
#        
#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['class'] = "form-control"
#         self.fields['password'].widget.attrs['class'] = "form-control"
#         self.fields['firstname'].widget.attrs['class'] = "form-control"
#         self.fields['lastname'].widget.attrs['class'] = "form-control"
#         self.fields['laboratory'].widget.attrs['class'] = "form-control"
#         self.fields['telnumber'].widget.attrs['class'] = "form-control"