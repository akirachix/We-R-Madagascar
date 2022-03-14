from django.urls import path
from .models import Schedule
from django.contrib.staticfiles.urls import urlpatterns

from .views import ScheduleFormView, scheduledShipmentsList,edit_shipment, delayedShipmentsList
app_name = "shipments"

urlpatterns = [
    path('scheduled/',scheduledShipmentsList , name='shipment'),
    path('schedule_shipments',ScheduleFormView.as_view(), name='schedule_shipments'),
    path('edit/<int:id>/',edit_shipment,name='edit_shipment'),
    path('delayed/',delayedShipmentsList , name='delayed_shipments'),


]