from django.db import models
from django.contrib import admin
import uuid

from api.twilio import Twilio

from registry.models import Aircraft
from flightres.utils import reverseGeocode

class FlightPermission(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    """This model is used for flight registration"""
    uav_uid = models.AutoField(primary_key=True)
    uav_uuid = models.ForeignKey("registry.Aircraft", to_field='unid', db_column='uav_uuid', related_name='uav_uuid', null=True, blank=True, on_delete=models.CASCADE)
    existing_permission_id = models.IntegerField(null=True, blank=True)
    flight_start_date = models.DateField(null=True, blank=True)
    flight_end_date = models.DateField(null=True, blank=True)
    flight_time = models.CharField(max_length=300, null=True, blank=True)
    flight_purpose = models.CharField(max_length=200, null=True, blank=True)
    flight_plan_url = models.URLField(max_length=200, null=True, blank=True)
    flight_insurance_url = models.URLField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    pilot_id = models.ForeignKey("flightres.Pilots", on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    status = models.TextField(choices = STATUS_CHOICES, default='Pending')
    location = models.URLField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    twilio = Twilio()

    def __init__(self, *args, **kwargs):
        super(FlightPermission, self).__init__(*args, **kwargs)
        self.old_status = self.status

    def save(self, force_insert=False, force_update=False, using=None):
        if self.uav_uuid != '' or self.uav_uuid != None:
            try:
                company = Aircraft.objects.get(id=self.uav_uuid.id)
            except Aircraft.DoesNotExist:
                pass
        if self.old_status != self.status:
            uri = "np/dashboard/request_response/"
            response_data = uri + str(self.uav_uid)
            message = "Your flight plan has been approved. You can find more details at {}".format(response_data)
            # self.twilio.send_message(self.pilot_phone_number, message)

        super().save(force_insert, force_update, using)

    def __str__(self):
        return str(self.uav_uid)


class Report(models.Model):
    STATUS_CHOICE = (
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved')
    )
    """This model is used for storing complaints sent via WhatsApp"""
    uav_uid = models.AutoField(primary_key=True)
    message = models.TextField(null=False, default='')
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    complainer_name = models.CharField(max_length=50, null=True, blank=True)
    complainer_number = models.CharField(max_length=30, blank=True, null=True)
    note = models.TextField(blank=True, null=True,unique=False)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=15, default='Pending')
    reply = models.TextField(default='', blank=True, null=True)
    category = models.TextField(default='', blank=True, null=True)
    is_escalated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    twilio = Twilio()

    def __init__(self, *args, **kwargs):
        super(Report, self).__init__(*args, **kwargs)
        self.old_reply = self.reply

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.old_reply != self.reply:
            self.twilio.send_message(self.complainer_number, self.reply)

        geo_reponse = reverseGeocode(self.location)
        if geo_reponse == "Inavalid Address":
            self.latitude = 0
            self.longitude = 0
        else:
            self.latitude = geo_reponse[0]
            self.longitude = geo_reponse[1]

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.uav_uid)


class Pilots(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=100,  null=True, blank=True)
    cv_url = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LocalAuthorities(models.Model):
    AUTHORITY_TYPES = (
        ('Police', 'Police'),
        ('Others', 'Others')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    authority_type = models.CharField(max_length=50, choices=AUTHORITY_TYPES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name