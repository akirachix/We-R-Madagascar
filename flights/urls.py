from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', RequestFlightView.as_view(), name='flight_request'),
    path('pending-flights/', PendingFlightRequestsListView.as_view(), name='pending_requests'),
    path('delayed-flights/', DelayedFlightRequestsListView.as_view(), name='delayed_requests'),
    path('scheduled-flights/', ScheduledFlightRequestsListView.as_view(), name='scheduled_requests'),
   
]