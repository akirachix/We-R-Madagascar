from rest_framework.routers import SimpleRouter
from api.views import FlightRegistryView, WhComplainView, SheetUploadView

router = SimpleRouter()
router.register(r'flightres', FlightRegistryView, 'FlighResAPI')
router.register(r'whcomplain', WhComplainView, 'WHComplaintAPI')
router.register(r'sheet-upload', SheetUploadView)

urlpatterns = router.urls
