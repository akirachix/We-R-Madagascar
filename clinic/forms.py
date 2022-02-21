from django.contrib.auth import models
from django.forms import fields, widgets
from .models import Clinic
from django import forms

class ClinicForm(forms.ModelForm):
    class Meta:
        model=Clinic
        fields='__all__'
        # widgets={
        #     "clinic_name":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic name"}),
        #     "phone_number":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic phone number"}),
        #     "location":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic location"}),
        #     "registration_number":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic registration number"})
        # }
  