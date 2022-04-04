from django.db import models

from django.utils import timezone

class FlightRequest(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Scheduled', 'Scheduled'),
        ('Delayed','Delayed')
    )

    clinic_name= models.CharField(max_length=50)
    total_volume = models.IntegerField()
    delivery_date = models.DateTimeField()
    priority_level = models.IntegerField()
    refrigration = models.BooleanField(choices=BOOL_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return self.clinic_name
