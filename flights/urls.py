from django.urls import path
from .views import *


urlpatterns=[
    path('request-flight/', RequestFlightView.as_view(), name='request_flight'),
   
]