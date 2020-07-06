from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, flightPermissionDetail, approvePerm

urlpatterns = [
    path('', FlightPermissionList.as_view(), name="dashboard"),
    path('approve_perm/<int:pk>/<str:action>', approvePerm, name='approve-perm'),
]
