from django.urls import path

# importing views from views..py
from .views import FlightPermissionList, approvePerm, flightReqResponseView, ComplainListView, dashboardView, \
        updateComplain, submitReply, AboutPageView, GuidelinesPageView, OperdatorDatabaseView, uploadSheet, denyPerm

urlpatterns = [
    path('', dashboardView, name='dashboard'),
    path('permission/<str:type>', FlightPermissionList.as_view(), name="permission"),
    path('approve_perm/<int:pk>/<str:action>',
         approvePerm, name='approve-perm'),
    path('deny_perm/<int:pk>',
         denyPerm, name='deny-perm'),
    path('upload_sheet', uploadSheet, name="upload-sheet"),
    path('request_response/<int:pk>',
         flightReqResponseView, name='request-response'),
    path('complain', ComplainListView.as_view(), name='complain-list'),
    path('update_complain/<int:pk>/<str:action>/<str:status>',
         updateComplain, name='update-complain'),
    path('submit_reply/<int:pk>', submitReply, name='submit-reply'),
    path('about', AboutPageView.as_view(), name='about'),
    path('guidelines', GuidelinesPageView.as_view(), name='guidelines'),
    path('operators', OperdatorDatabaseView.as_view(), name='operators'),
]
