from django.db import models
from django.utils import timezone

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(blank=True,null=True)
    location = models.CharField(max_length=50,null=True)
    district = models.CharField(max_length=300,null=True)
    contact=models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.clinic_name