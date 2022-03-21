from .models import Schedule
from django.db.models import fields
from django import forms
import datetime as dt
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('shipment_id','clinic_name','medication','units','delivery_date','take_of_time','delivery_time','status','destination',)
        widgets = {
            'shipment_id': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'clinic_name': forms.TextInput( attrs={'class': 'form-control','style':'width:50%',}),
            'medication':  forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'units': forms.NumberInput(attrs={'class': 'form-control','style':'width:50%'}),  
            'delivery_date': forms.DateInput( attrs={'class': 'form-control','style':'width:50%'}),

          
            'take_of_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'delivery_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'status': forms.Select( attrs={'class': 'form-control','style':'width:50%'}),

            'destination': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
           
        }
       
        labels={
            'shipment_id':' Shipment Id',
            'clinic_name': ' Clinic Name',
            'medication':'Medication',
            'units':'Units',
            'take_of_time':'Take of_time',
            'delivery_time':' Delivery Time',
            'status':' Status',
            'destination':' Destination',
       


        }



class DelayedForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('shipment_id','clinic_name','medication','units','delivery_date','take_of_time','delivery_time','status','destination','delay_reasons')
        widgets = {
            'shipment_id': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'clinic_name': forms.TextInput( attrs={'class': 'form-control','style':'width:50%',}),
            'medication':  forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'units': forms.NumberInput(attrs={'class': 'form-control','style':'width:50%'}), 
            'delivery_date': forms.DateInput( attrs={'class': 'form-control','style':'width:50%'}),

           
            'take_of_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'delivery_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'status': forms.Select( attrs={'class': 'form-select','style':'width:50%'}),

            'destination': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'delay_reasons': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
           
        }
       
        labels={
            'shipment_id':' Shipment Id',
            'clinic_name': ' Clinic Name',
            'medication':'Medication',
            'units':'Units',
            'take_of_time':'Take of_time',
            'delivery_time':' Delivery Time',
            'status':' Status',
            'destination':' Destination',
            'delay_reasons': 'Delay reasons',
       


        }
class RescheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('shipment_id','clinic_name','medication','units','delivery_date','take_of_time','delivery_time','status','destination','delay_reasons')
        widgets = {
            'shipment_id': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'clinic_name': forms.TextInput( attrs={'class': 'form-control','style':'width:50%',}),
            'medication':  forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'units': forms.NumberInput(attrs={'class': 'form-control','style':'width:50%'}),
            'delivery_date': forms.DateInput( attrs={'class': 'form-control','style':'width:50%'}),

            
            'take_of_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'delivery_time': forms.TimeInput( attrs={'class': 'form-control','style':'width:50%'}),
            'status': forms.Select( attrs={'class': 'form-select','style':'width:50%'}),

            'destination': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),
            'delay_reasons': forms.TextInput( attrs={'class': 'form-control','style':'width:50%'}),

           
        }
       
        labels={
            'shipment_id':' Shipment Id',
            'clinic_name': ' Clinic Name',
            'medication':'Medication',
            'units':'Units',
            'take_of_time':'Take of_time',
            'delivery_time':' Delivery Time',
            'status':' Status',
            'destination':' Destination',
            'delay_reasons': 'Delay reasons',

       


        }

