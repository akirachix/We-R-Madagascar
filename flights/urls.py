from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', RequestFlightView.as_view(), name='flight_request'),
    path('pending-flights/', PendingFlightRequestsListView.as_view(), name='pending_requests'),
   
]