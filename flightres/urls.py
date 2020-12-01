from django.urls import path
from . import views
# importing views from views..py
from .views import FlightPermissionList, approvePerm, flightReqResponseView, ComplainListView, dashboardView, \
    updateComplain, submitReply, AboutPageView, GuidelinesPageView, OperdatorDatabaseView, denyPerm, \
    assignPerm, bulkupload, FlightView , OperatorAddView

urlpatterns = [
    path('', dashboardView, name='dashboard'),
    path('permission/<str:type>', FlightPermissionList.as_view(), name="permission"),
    path('allflights', FlightView.as_view(), name="flightview"),
    path('approve_perm/<int:pk>/<str:action>',
         approvePerm, name='approve-perm'),
    path('deny_perm/<int:pk>',
         denyPerm, name='deny-perm'),
    path('assign_perm/<int:pk>/<str:action>',
         assignPerm, name='assign-perm'),
    # path('upload_sheet', uploadSheet, name="upload-sheet"),
    path('request_response/<int:pk>',
         flightReqResponseView, name='request-response'),
    path('complain', ComplainListView.as_view(), name='complain-list'),
    path('update_complain/<int:pk>/<str:action>/<str:status>',
         updateComplain, name='update-complain'),
    path('submit_reply/<int:pk>', submitReply, name='submit-reply'),
    path('about', AboutPageView.as_view(), name='about'),
    path('guidelines', GuidelinesPageView.as_view(), name='guidelines'),
    path('operators', OperdatorDatabaseView.as_view(), name='operators'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('upload_sheet-new', bulkupload, name="upload-sheet-new"),
    path('upload_data', views.dronedataupload, name="upload-data"),
    path('edit_data/<uuid:pk>', views.dronedataupdate, name="data-edit"),
    path('add_operator', OperatorAddView.as_view(), name="add-operator")

]
