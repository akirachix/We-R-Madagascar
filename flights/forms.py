from django.contrib.auth import models
from django.forms import fields, widgets
from .models import FlightRequest
from django import forms

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)
class RequestFlightForm(forms.ModelForm):
   
    class Meta:
        model=FlightRequest
        fields=['clinic_name','total_volume','delivery_date','priority_level','refrigration']
        widgets={
            "clinic_name":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter clinic name"}),
            "total_volume":forms.TextInput(attrs={'class':'form-control','style':'width:100%',"placeholder":"Enter no. of litres"}),
            "delivery_date":forms.DateInput(format=('%d/%m/%Y'),attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),
            "priority_level":forms.TextInput(attrs={'class':'form-control','style':'width:100%'}),
            "refrigration":forms.Select(choices=TRUE_FALSE_CHOICES),
            # "status" = models.CharField(max_length=30, choices=STATUS_CHOICES,default='pending')
        }

   