from django.db import models

STATUS_CHOICES = (
 ('pending','pending'),
 ('processed', 'processed'),
 ('dispatched','dispatched'),
)
# Create your models here.
class Schedule(models.Model):
    shipment_id = models.CharField(max_length=7)
    clinic_name = models.CharField(max_length=20)
    medication = models.CharField(max_length=20)
    units = models.CharField(max_length=5)
    delivery_date = models.DateField()
    take_of_time= models.DateField()
    delivery_time = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='dispatched')
    destination = models.CharField(max_length=20)

    def __str__(self):
        return self.shipment_id

class Delayed(models.Model):
    shipment_id = models.CharField(max_length=7)
    clinic_name = models.CharField(max_length=20)
    medication = models.CharField(max_length=20)
    units = models.CharField(max_length=5)
    delivery_date = models.DateField()
    take_of_time= models.DateField()
    delivery_time = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='dispatched')
    destination = models.CharField(max_length=20)
    delay_reasons = models.CharField(max_length=50)
