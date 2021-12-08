from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from authentication.views import ObtainTokenPairWithUserDetail, CustomUserCreate,ClinicCreateView,ClinicViewDetails,ClinicUpdateView

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('token/obtain/', ObtainTokenPairWithUserDetail.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/register-clinic/', ClinicCreateView.as_view(), name='register_clinic'),
    path('token/view-clinics/', ClinicViewDetails.as_view(), name='view_clinic'),
    path('token/edit-clinic/<int:pk>/', ClinicUpdateView.as_view(), name='edit_clinic'),


]