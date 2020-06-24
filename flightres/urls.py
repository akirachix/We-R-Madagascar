from django.urls import path

# importing views from views..py
from .views import FlightPermissionList

urlpatterns = [
    path('', FlightPermissionList.as_view(), name="dashboard"),
]
