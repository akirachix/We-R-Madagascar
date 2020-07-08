from django.urls import path

from whatsappmsg import views
from api.views import date_validation_view, UniqueTeatDataView

urlpatterns = [
    path('test/', views.reply_whatsapp),
    path('date/val/', date_validation_view),
    path('unid/val/', UniqueTeatDataView.as_view())
]
