from django.db import models

from clinic.models import Clinic

class FlightRequest(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Scheduled', 'Scheduled'),
        ('Delayed','Delayed'),
        ('Completed','Completed'),
        ('Processed','Processed'),
        ('Dispatched','Dispatched'),

    )

    clinic_name= models.ForeignKey(Clinic,on_delete=models.CASCADE)
    total_volume = models.IntegerField()
    delivery_date = models.DateTimeField()
    priority_level = models.IntegerField()
    medication = models.CharField(max_length=300,null=True, blank=True)
    refrigration = models.BooleanField(choices=BOOL_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='Pending')
    delayed_reasons = models.CharField(max_length=300, null=True)
    last_updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clinic_name.clinic_name
