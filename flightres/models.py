from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib import admin
#from django.db.models.signals import post_save
import uuid
from django.contrib.auth.models import User
import geopandas
from api.twilio import Twilio
import base64
from registry.models import Aircraft
from flightres.utils import reverseGeocode
from ohio import settings
from zipfile import ZipFile


class FlightPermission(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    """This model is used for flight registration"""
    uav_uid = models.AutoField(primary_key=True)
    uav_uuid = models.ForeignKey("registry.Aircraft", to_field='unid', db_column='uav_uuid', related_name='uav_uuid',
                                 null=True, blank=True, on_delete=models.CASCADE)
    existing_permission_id = models.IntegerField(null=True, blank=True)
    flight_start_date = models.DateField(null=True, blank=True)
    flight_end_date = models.DateField(null=True, blank=True)
    flight_time = models.CharField(max_length=300, null=True, blank=True)
    flight_purpose = models.CharField(max_length=200, null=True, blank=True)
    flight_plan_url = models.URLField(max_length=200, null=True, blank=True)
    flight_insurance_url = models.URLField(
        max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    pilot_id = models.ForeignKey(
        "flightres.Pilots", on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=20, decimal_places=10, null=True, blank=True)
    altitude = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='Pending')
    rejection_reason = models.TextField(null=True, blank=True)
    location = models.URLField(max_length=200, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    db_index=True, on_delete=models.SET_NULL, related_name="assigned_to")
    created_date = models.DateTimeField(auto_now_add=True)
    is_special_permission = models.BooleanField(default=False)

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

            uri = "https://droneregistry.naxa.com.np/np/dashboard/request_response/"
            msg1 = str(self.uav_uid)
            msg2 = str(self.status)
            msg1_enc = msg1.encode('ASCII')
            msg1_crypt = base64.b64encode(msg1_enc)
            msg1_crypt_str = msg1_crypt.decode('ASCII')
            msg2_enc = msg2.encode('ASCII')
            msg2_crypt = base64.b64encode(msg2_enc)
            msg2_crypt_str = msg2_crypt.decode('ASCII')
            fin_msg = msg1_crypt_str + '$' + msg2_crypt_str
            response_data = uri + fin_msg
            message = "Your flight permission request has a update. Open this link to find out more {}".format(
                response_data)
            try:
                self.twilio.send_message(self.pilot_id.phone_number, message)
            except:
                print("error")

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
    latitude = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    complainer_name = models.CharField(max_length=50, null=True, blank=True)
    complainer_number = models.CharField(max_length=30, blank=True, null=True)
    note = models.TextField(blank=True, null=True, unique=False)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICE,
                              max_length=15, default='Pending')
    reply = models.TextField(blank=True, null=True, unique=False)
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
            self.twilio.send_report_reply(
                self.complainer_number, self.reply, self.category, self.message)

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
    company = models.CharField(max_length=100, null=True, blank=True)
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
    latitude = models.DecimalField(
        max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=20, decimal_places=10, null=True, blank=True)
    authority_type = models.CharField(
        max_length=50, choices=AUTHORITY_TYPES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NoFlyZone(models.Model):

    spatialdata_zip_file = models.FileField(upload_to='shp_files', blank=True, null=True)
    

    def save(self, *args, **kwargs):
        with ZipFile(self.spatialdata_zip_file, 'r') as zipped:
            dat = str(self.spatialdata_zip_file)
            datpath = str(self.spatialdata_zip_file.path)
            for x in zipped.namelist():
                if x.endswith('.shp'):
                    outfile = open(datpath.replace(dat, '') + 'shp_files/' + x, 'wb')
                    outfile.write(zipped.read(x))
                    outfile.close()
                    shpname = datpath.replace(dat, '') + 'shp_files/' + x
                elif x.endswith('.shx'):
                    outfile = open(datpath.replace(dat, '') + 'shp_files/' + x, 'wb')
                    outfile.write(zipped.read(x))
                    outfile.close()
        myshpfile = geopandas.read_file(shpname, encoding='ISO8859-1')
        myshpfile.to_file(shpname.replace('.shp', '.geojson'), driver='GeoJSON')
        super(NoFlyZone, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.spatialdata_zip_file).replace('shp_files/', '')
'''def create_geojson(sender, **kwargs):
    if kwargs['created']:
        full_path = kwargs['instance'].shp_file.path
        
        myshpfile = geopandas.read_file(full_path, encoding='ISO8859-1')
        myshpfile.to_file('uploads/'+ str(kwargs['instance'].shp_file).replace('.shp', '.geojson'), driver='GeoJSON')

post_save.connect(create_geojson, sender=NoFlyZone)'''
    



    