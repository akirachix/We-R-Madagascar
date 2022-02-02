# from django.urls import path
# from .views import *


# urlpatterns=[
#     path('register-clinic/', ClinicCreateView.as_view(), name='register_clinic'),
#     path('view-clinics/', ClinicViewDetails.as_view(), name='view_clinic'),
#     path('edit-clinic/<int:pk>/', ClinicUpdateView.as_view(), name='edit_clinic'),
#     # path('search/', views.search_clinic, name='search'),
# ]

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from clinic.views import clinic_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', clinic_upload, name='clinic_upload'),
]