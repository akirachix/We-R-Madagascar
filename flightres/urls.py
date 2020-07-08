from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, approvePerm, flightReqResponseView, ComplainListView, dashboardView, updateComplain, submitReply

urlpatterns = [
    path('', dashboardView, name='dashboard'),
    path('flightperm_list', FlightPermissionList.as_view(), name="flightperm-list"),
    path('approve_perm/<int:pk>/<str:action>', approvePerm, name='approve-perm'),
    path('request_response/<int:pk>', flightReqResponseView, name='request-response'),
    path('complain_list', ComplainListView.as_view(), name='complain-list'),
    path('update_complain/<int:pk>/<str:action>', updateComplain, name='update-complain'),
    path('submit_reply/<int:pk>', submitReply ,name='submit-reply')
]
