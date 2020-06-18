from django.contrib import admin
from .models import Report, FlightPermission, FlightRegistryAdmin, WhatsappComplainAdmin

admin.site.register(Report, WhatsappComplainAdmin)
admin.site.register(FlightPermission, FlightRegistryAdmin)



