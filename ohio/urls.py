"""ohio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler400, handler404, handler500
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from registry import views as registryviews
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView, LogoutView
from flightres.views import homeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
import django.views.static

# from registry.views import UserViewSet

handler404 = 'flightres.views.view_404'
handler500 = 'flightres.views.view_500'

admin.autodiscover()
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views

# schema_view = get_schema_view(
#    openapi.Info(
#       title="DroneRes API",
#       default_version='v1',
#       description="Test APIs for dashboard",
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeView, name='home'),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/v1/', registryviews.APIView.as_view()),
    path('api/v1/operators', registryviews.OperatorList.as_view()),
    path('api/v1/operators/<uuid:pk>', registryviews.OperatorDetail.as_view()),
    path('api/v1/operators/<uuid:pk>/privilaged', registryviews.OperatorDetailPrivilaged.as_view()),
    path('api/v1/operators/<uuid:pk>/rpas', registryviews.OperatorAircraft.as_view()),
    path('api/v1/aircraft/<esn>', registryviews.AircraftESNDetails.as_view()),
    path('api/v1/contacts', registryviews.ContactList.as_view()),
    path('api/v1/contacts/<uuid:pk>', registryviews.ContactDetail.as_view()),
    path('api/v1/contacts/<uuid:pk>/privilaged', registryviews.ContactDetailPrivilaged),
    path('api/v1/operators/<uuid:pk>/aircraft', registryviews.OperatorAircraft.as_view()),
    path('api/v1/pilots', registryviews.PilotList.as_view()),
    path('api/v1/pilots/<uuid:pk>', registryviews.PilotDetail.as_view()),
    path('api/v1/pilots/<uuid:pk>/privilaged', registryviews.PilotDetailPrivilaged.as_view()),
    path('whatsapp/', include('whatsappmsg.urls')),
    path('api/v1/user/', include('authentication.urls')),
    path('np/clinic/', include('clinic.urls')),
    path('np/flights/', include('flights.urls')),
    path('np/api/v1/', include('api.urls')),
    path('np/shipments/',include(('shipments.urls', 'shipments'), namespace="shipment")),
    path('np/dashboard/', include(('flightres.urls', 'flightres'), namespace='dashboard')),
    url(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-token-auth/', obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
