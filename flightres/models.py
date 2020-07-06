from django.db import models
from django.contrib import admin
import uuid

from api.twilio import Twilio


class FlightPermission(models.Model):
    """This model is used for flight registration"""
    uav_uid = models.AutoField(primary_key=True)
    uav_uuid = models.CharField(max_length=20, null=True, blank=True)
    flight_start_date = models.CharField(max_length=300, null=True, blank=True)
    flight_end_date = models.CharField(max_length=300, null=True, blank=True)
    flight_time = models.CharField(max_length=300, null=True, blank=True)
    flight_purpose = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    # flight_plan = models.FileField(upload_to='uploads/FlightPlan')
    # flight_insurance = models.FileField(upload_to='uploads/Insurance')
    pilot_name = models.CharField(max_length=50, null=True, blank=True)
    pilot_phone_number = models.CharField(max_length=50, null=True, blank=True)
    # pilot_cv = models.FileField(upload_to='uploads/PilotCV')
    pilot_cv_url = models.URLField(max_length=200, null=True, blank=True)
    flight_plan_url = models.URLField(max_length=200, null=True, blank=True)
    flight_insurance_url = models.URLField(max_length=200, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    twilio = Twilio()

    def __init__(self, *args, **kwargs):
        super(FlightPermission, self).__init__(*args, **kwargs)
        self.old_is_approved = self.is_approved

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.old_is_approved != self.is_approved:
            print("SENDING" + self.pilot_phone_number)
            uri = "np/api/v1/flightres/"
            response_data = uri + str(self.uav_uid)
            print(response_data)
            message = "Your flight plan has been approved. You can find more details at xyz.com/details/1"
            # self.twilio.send_message(self.pilot_phone_number, message)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.uav_uid)


class FlightRegistryAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'pilot_name', 'pilot_phone_number')
    search_fields = ['uav_uid', 'pilot_name']


class Report(models.Model):
    """This model is used for storing complaints sent via WhatsApp"""
    uav_uid = models.AutoField(primary_key=True)
    message = models.TextField(null=False, default='')
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    complainer_name = models.CharField(max_length=50, null=True, blank=True)
    complainer_number = models.CharField(max_length=30, blank=True, null=True)
    # photo = models.FileField(upload_to='uploads/WhComplains', blank=True, null=True)
    # note = models.TextField(blank=True, null=True,unique=False)
    image_url = models.URLField(max_length=200, null=True, blank=True)

    reply = models.TextField(default='')
    category = models.TextField(default='')
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

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "self.uav_uid"


class WhatsappComplainAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'complainer_name', 'complainer_number', 'message', 'reply')
    search_fields = ['uav_uid', 'complainer_name']
