from django.urls import path
from .models import Schedule
from django.contrib.staticfiles.urls import urlpatterns

from .views import update, edit_shipment,scheduledShipmentsList,checkDelayedShipments,edit_delay,checkCompletedShipments,completed_profile,search_clinic
app_name = "shipments"

urlpatterns = [
    path('scheduled/',scheduledShipmentsList , name='shipment'),

    path('search_shipments/',search_clinic,name='search_shipment'),
    path('schedule_shipments',update, name='schedule_shipments'),
    path('edit/<int:id>/',edit_shipment,name='edit_shipment'),
    path('delayed/',checkDelayedShipments , name='delayed_shipments'),
    path('reschedule/<int:id>/',edit_delay,name='edit_delays'),
    path('completed/',checkCompletedShipments , name='completed_shipments'),
    path('profile/<int:id>/',completed_profile,name='completed_profile'),





]