from django.contrib import admin
from .models import Report, FlightPermission, Pilots

class FlightRegistryAdmin(admin.ModelAdmin):
    list_display = ['uav_uid', 'company_name', 'status']
    search_fields = ['uav_uid',]

class WhatsappComplainAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'complainer_name', 'complainer_number', 'message', 'reply')
    search_fields = ['uav_uid', 'complainer_name']

class PilotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company']
    search_fields = ['id', 'name']

admin.site.register(Report, WhatsappComplainAdmin)
admin.site.register(FlightPermission, FlightRegistryAdmin)
admin.site.register(Pilots, PilotsAdmin)



