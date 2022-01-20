from django.contrib import admin
#from leaflet.admin import LeafletGeoAdmin
from .models import Report, FlightPermission, Pilots, LocalAuthorities, NoFlyZone, PermissionLogs, ReportsLogs

class FlightRegistryAdmin(admin.ModelAdmin):
    list_display = ['uav_uid', 'company_name', 'status', 'latitude', 'longitude']
    search_fields = ['uav_uid',]

class WhatsappComplainAdmin(admin.ModelAdmin):
    list_display = ('uav_uid', 'complainer_name', 'complainer_number', 'message', 'reply')
    search_fields = ['uav_uid', 'complainer_name']

class PilotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company']
    search_fields = ['id', 'name']

class LocalAuthoritiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number']
    search_fields = ['id', 'name', 'phone_number']

class NoFlyZoneAdmin(admin.ModelAdmin):
    pass
    #exclude = ('shp_file', 'shx_file',)

class PermissionLogsAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission_id', 'status', 'created_at', 'updated_at']

class ReportsLogsAdmin(admin.ModelAdmin):
    list_display = ['user', 'complaint_id', 'status', 'escalate', 'note', 'reply', 'created_at', 'updated_at']

admin.site.register(Report, WhatsappComplainAdmin)
admin.site.register(FlightPermission, FlightRegistryAdmin)
admin.site.register(Pilots, PilotsAdmin)
admin.site.register(LocalAuthorities, LocalAuthoritiesAdmin)
admin.site.register(NoFlyZone, NoFlyZoneAdmin)
admin.site.register(PermissionLogs, PermissionLogsAdmin)
admin.site.register(ReportsLogs, ReportsLogsAdmin)


