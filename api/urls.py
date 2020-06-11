from rest_framework.routers import SimpleRouter
from api.views import FlightRegistryView, WhComplainView

router = SimpleRouter()

router.register(r'flightres', FlightRegistryView, 'FlighResAPI')
router.register(r'whcomplain', WhComplainView, 'WHComplaintAPI')

urlpatterns = router.urls