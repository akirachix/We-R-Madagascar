from .models import Schedule, Delayed
from django.db.models import fields
from django import forms

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = '__all__'
class DelayedForm(forms.ModelForm):
    class Meta:
        model = Delayed
        fields = '__all__'
