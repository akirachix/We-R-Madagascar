from django.contrib import admin
from .models import Authorization, Activity, Operator, Contact, Aircraft, Person, \
    Address, Pilot, Complain, Manufacturer, SheetRegister

class OperatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'address']
    search_fields = ['id', 'company_name']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']
    search_fields = ['id']

class AircraftAdmin(admin.ModelAdmin):
    list_display = ['id', 'popular_name', 'mass', 'operator']
    search_fields = ['id', 'popular_name']

admin.site.register(Authorization)
admin.site.register(Activity)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Contact)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Pilot)
admin.site.register(Complain)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(SheetRegister)
