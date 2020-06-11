from django.contrib import admin
from .models import WhatsappComplain, FlightRegistry, FlightRegistryAdmin, WhatsappComplainAdmin

admin.site.register(WhatsappComplain, WhatsappComplainAdmin)
admin.site.register(FlightRegistry, FlightRegistryAdmin)



