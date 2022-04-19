from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', request_flight, name='flight_request'),
    path('pending-flights/',PendingRequestsView.as_view(), name='pending_requests'),
    path('delayed-flights/', delayed_flights, name='delayed_requests'),
    path('scheduled-flights/', scheduled_requests, name='scheduled_requests'),
    # path('delayed-reason-form/<int:id>/',delayed_reason_request,name='delayed_reason_form'),
   
]
