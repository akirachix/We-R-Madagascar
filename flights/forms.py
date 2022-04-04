from django.contrib.auth import models
from django.forms import fields, widgets
from .models import FlightRequest
from django import forms

class RequestFlightForm(forms.ModelForm):
    class Meta:
        model=FlightRequest
        fields='__all__'
        widgets={
            "clinic_name":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic name"}),
            "total_volume":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter no. of litres"}),
            "delivery_date":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"select delivery date"}),
            "priority_level":forms.TextInput(attrs={'class':'form-control','style':'width:100%'}),
            "refrigration":forms.TextInput(attrs={'class':'form-control','style':'width:100%'})
        }

   