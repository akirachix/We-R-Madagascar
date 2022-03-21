
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', clinic_upload, name='clinic_upload'),
    path('view-clinics/', ClinicViewDetails.as_view(), name='view_clinics'),
    path('search-clinic/', search_clinic, name='search_clinic'),
]
    