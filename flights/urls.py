from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', request_flight, name='flight_request'),
    path('pending-flights/',PendingRequestsView.as_view(), name='pending_requests'),
    path('delayed-flights/', delayed_flights, name='delayed_requests'),
    path('scheduled-flights/', scheduled_requests, name='scheduled_requests'),
   
]