from tkinter import CENTER
from django.db import models
from django.utils import timezone

class Clinic(models.Model):
    pays = models.CharField(max_length=50)
    region = models.EmailField(blank=True)
    district = models.CharField(max_length=70)
    commune = models.CharField(max_length=100)
    center = models.CharField(max_length=100)
    UID_centre = models.CharField(max_length=50)
    latitude =  models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        return self.name