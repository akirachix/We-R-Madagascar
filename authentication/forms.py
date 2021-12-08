from django.contrib.auth import models
from django.forms import fields, widgets
from .models import ClinicProfile
from django import forms

class RegisterclinicForm(forms.ModelForm):
    class Meta:
        model=ClinicProfile
        fields='__all__'
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control','style':'width:100%'}),
            "phone_number":forms.TextInput(attrs={'class':'form-control','style':'width:100%'}),
            "location":forms.TextInput(attrs={'class':'form-control','style':'width:100%'})
        }