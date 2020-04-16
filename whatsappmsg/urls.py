from django.urls import path

from whatsappmsg import views

urlpatterns = [
    path('test/', views.reply_whatsapp)
]