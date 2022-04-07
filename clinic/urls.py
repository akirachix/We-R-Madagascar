
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from clinic.views import clinic_upload,clinic_display,search_clinic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', clinic_upload, name='clinic_upload'),
    path('view-clinics/', clinic_display, name='view_clincs'),
    path('search-clinic/', search_clinic, name='search_clinic'),
]