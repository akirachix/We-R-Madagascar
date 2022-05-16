from django.urls import path
from .models import Schedules
from django.contrib.staticfiles.urls import urlpatterns

from .views import  edit_shipment,scheduledShipmentsList,checkDelayedShipments,edit_delay,checkCompletedShipments,completed_profile
app_name = "shipments"

urlpatterns = [
    path('scheduled/',scheduledShipmentsList , name='shipment'),
    # path('schedule_shipments',ScheduleFormView.as_view(), name='schedule_shipments'),
    path('edit/<int:id>/',edit_shipment,name='edit_shipment'),
    path('delayed/',checkDelayedShipments , name='delayed_shipments'),
    path('reschedule/<int:id>/',edit_delay,name='edit_delays'),
    path('completed/',checkCompletedShipments , name='completed_shipments'),
    path('profile/<int:id>/',completed_profile,name='completed_profile'),





]