from .models import Schedule
from django.db.models import fields
from django import forms
import datetime as dt
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('shipment_id','clinic_name','medication','units','delivery_date','take_of_time','delivery_time','status','destination',)
        widgets = {'take_of_time': forms.Select(choices=HOUR_CHOICES)}
        widgets = {'delivery_time': forms.Select(choices=HOUR_CHOICES)}


class DelayedForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'take_of_time': forms.Select(choices=HOUR_CHOICES)}
        widgets = {'delivery_time': forms.Select(choices=HOUR_CHOICES)}

class RescheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'take_of_time': forms.Select(choices=HOUR_CHOICES)}
        widgets = {'delivery_time': forms.Select(choices=HOUR_CHOICES)}

