from django.db import models
from django.db.models.signals import post_save
import datetime as dt



STATUS_CHOICES = (
 ('Pending','Pending'),
 ('Processed', 'Processed'),
 ('Dispatched','Dispatched'),
 ('Delayed','Delayed'),
 ('Completed','Completed'),

)
# Create your models here.
class Schedule(models.Model):
    shipment_id = models.CharField(max_length=7)
    clinic_name = models.CharField(max_length=20)
    medication = models.CharField(max_length=20)
    units = models.CharField(max_length=5)
    delivery_date = models.DateField()
    take_of_time= models.TimeField(default=dt.time(00, 00))
    delivery_time = models.TimeField(default=dt.time(00, 00))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='dispatched')
    destination = models.CharField(max_length=20)
    delay_reasons= models.CharField(max_length=20,default='Air Traffic')




    def __str__(self):
        return self.status



