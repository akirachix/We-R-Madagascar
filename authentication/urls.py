from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from authentication.views import ObtainTokenPairWithUserDetail, CustomUserCreate

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('token/obtain/', ObtainTokenPairWithUserDetail.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]