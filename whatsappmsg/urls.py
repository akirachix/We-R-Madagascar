from django.urls import path

from whatsappmsg import views
from api.views import date_validation_view, UniqueTeatDataView, OldPermissionIdValidation, GeoLocationValidation

urlpatterns = [
    path('test/', views.reply_whatsapp),
    path('date/val/', date_validation_view),
    path('unid/val/', UniqueTeatDataView.as_view()),
    path('perm/val/', OldPermissionIdValidation.as_view()),
    path('geo/val/', GeoLocationValidation.as_view())
]
