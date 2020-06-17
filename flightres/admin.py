from django.contrib import admin
from .models import Report, FlightRegistry, FlightRegistryAdmin, WhatsappComplainAdmin

admin.site.register(Report, WhatsappComplainAdmin)
admin.site.register(FlightRegistry, FlightRegistryAdmin)



