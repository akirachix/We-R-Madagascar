from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, approvePerm, flightReqResponseView

urlpatterns = [
    path('', FlightPermissionList.as_view(), name="dashboard"),
    path('approve_perm/<int:pk>/<str:action>', approvePerm, name='approve-perm'),
    path('request_response/<int:pk>', flightReqResponseView, name='request-response'),

urlpatterns = [
    path('', FlightPermissionList.as_view(), name="dashboard"),
    path('flightperm_detail/<int:pk>', flightPermissionDetail, name='flightperm-detail'),
    path('approve_perm/<int:pk>/<str:action>', approvePerm, name='approve-perm'),
