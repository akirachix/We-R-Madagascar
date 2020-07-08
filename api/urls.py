from rest_framework.routers import SimpleRouter
from api.views import FlightRegistryView, WhComplainView, SheetUploadView, \
    UniqueTeatDataView
from django.urls import path, include

router = SimpleRouter()
router.register(r'flightres', FlightRegistryView, 'FlighResAPI')
router.register(r'whcomplain', WhComplainView, 'WHComplaintAPI')
router.register(r'sheet-upload', SheetUploadView)

urlpatterns = [
    path('', include(router.urls)),
]
