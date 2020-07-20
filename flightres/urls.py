from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, approvePerm, flightReqResponseView, ComplainListView, dashboardView, \
        updateComplain, submitReply, AboutPageView, GuidelinesPageView, OperdatorDatabaseView

urlpatterns = [
    path('', dashboardView, name='dashboard'),
    path('permission', FlightPermissionList.as_view(), name="permission"),
    path('approve_perm/<int:pk>/<str:action>',
         approvePerm, name='approve-perm'),
    path('request_response/<int:pk>',
         flightReqResponseView, name='request-response'),
    path('complain', ComplainListView.as_view(), name='complain-list'),
    path('update_complain/<int:pk>/<str:action>',
         updateComplain, name='update-complain'),
    path('submit_reply/<int:pk>', submitReply, name='submit-reply'),
    path('about', AboutPageView.as_view(), name='about'),
    path('guidelines', GuidelinesPageView.as_view(), name='guidelines'),
    path('operators', OperdatorDatabaseView.as_view(), name='operators'),
]
