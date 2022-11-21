from django.contrib import admin
from flights import models

# Register your models here.

@admin.register(models.FlightRequest)
class FlightRequestAdmin(admin.ModelAdmin):
    list_display = ('clinic_name','status','last_updated')
    readonly_fields=('last_updated',)