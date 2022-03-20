from django.contrib.auth import models
from django.forms import fields, widgets
from .models import Clinic
from django import forms

class ClinicForm(forms.ModelForm):
    class Meta:
        model=Clinic
        fields='__all__'
      
  