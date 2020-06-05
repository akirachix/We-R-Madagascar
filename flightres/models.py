from django.db import models
from django.contrib import admin
import  uuid

class FlightRegistry(models.Model):
    '''This model is used for flight resgistration'''
    uav_uid = models.CharField(max_length=20, primary_key=True)
    flight_date = models.DateTimeField()
    flight_purpose = models.CharField(max_length=200)
    flight_plan = models.FileField(upload_to='uploads/FlightPlan')
    flight_insurance = models.FileField(upload_to='uploads/Insurance')
    pilot_name = models.CharField(max_length=50)
    pilot_phone_number =models.CharField(max_length=15)
    pilot_cv = models.FileField(upload_to='uploads/PilotCV')

    def __str__(self):
        return self.uav_uid
    

class FlightRegistryAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'pilot_name', 'pilot_phone_number')
    search_fields = ['uav_uid','pilot_name']

class WhatsappComplain(models.Model):
    """This model is used for storing complaints sent via whatsapp"""
    uav_uid = models.CharField(max_length=20, primary_key=True)
    message = models.TextField(null=False, default='')
    location = models.CharField(max_length=100)
    latitude = models. DecimalField(max_digits=9, decimal_places=6)
    longitude = models. DecimalField(max_digits=9, decimal_places=6)
    complainer_name = models.CharField(max_length=50, null=False, blank=False)
    complainer_number = models.CharField(max_length=15)
    photo = models.FileField(upload_to='uploads/WhComplains')
    note = models.TextField()
    reply = models.TextField(default='')
    is_escalated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uav_uid

class WhatsappComplainAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'complainer_name', 'complainer_number', 'message', 'reply')
    search_fields = ['uav_uid','complainer_name']