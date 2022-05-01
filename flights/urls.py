from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', request_flight, name='flight_request'),
    path('pending-flights/',PendingRequestsView.as_view(), name='pending_requests'),
    path('scheduled-flights/',ScheduleRequestsView.as_view(), name='scheduled_requests'),
    path('delayed-flights/', DelayedFlightsView.as_view(), name='delayed_requests'),
    
    
   
]
