from rest_framework.routers import SimpleRouter
from api.views import FlightRegistryView, WhComplainView, SheetUploadView, \
    UniqueTeatDataView, PilotDetailAPIView, GetPilotFromPermissionView
from django.urls import path, include

import twilio
router = SimpleRouter()
router.register(r'flightres', FlightRegistryView, 'FlighResAPI')
router.register(r'whcomplain', WhComplainView, 'WHComplaintAPI')
router.register(r'sheet-upload', SheetUploadView, 'SheetUploadAPI')
router.register(r'pilot-data', PilotDetailAPIView, 'PilotDataAPI')
router.register(r'pilot-from-perm', GetPilotFromPermissionView, 'PilotFromPermAPI')

urlpatterns = [
    path('', include(router.urls)),
]
