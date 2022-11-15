from django.db import models
from django.db.models.signals import post_save
import datetime as dt

from django.utils import timezone
from clinic.models import Clinic

STATUS_CHOICES = (
 ('Pending','Pending'),
 ('Processed', 'Processed'),
 ('Dispatched','Dispatched'),
 ('Delayed','Delayed'),
 ('Completed','Completed'),

)
# Create your models here.
class Schedule(models.Model):
    clinic_name = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    medication = models.CharField(max_length=20)
    units = models.CharField(max_length=5)
    delivery_date =models.DateTimeField()
    take_of_time=  models.TimeField(default=dt.time(00, 00))
    delivery_time =  models.TimeField(default=dt.time(00, 00))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='dispatched')
    destination = models.CharField(max_length=20)
    delay_reasons= models.CharField(max_length=20,default='Air Traffic')



    def __str__(self):
        return self.clinic_name.clinic_name



