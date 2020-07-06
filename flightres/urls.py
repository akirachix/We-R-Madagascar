from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, approvePerm, verifiedFlightresView

urlpatterns = [
    path('', FlightPermissionList.as_view(), name="dashboard"),
    path('approve_perm/<int:pk>/<str:action>', approvePerm, name='approve-perm'),
    path('flightres/<int:pk>', verifiedFlightresView, name='verified-flightres-view'),
]
