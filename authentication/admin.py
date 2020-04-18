from django.contrib import admin

# Register your models here.
from authentication.models import UserProfile, User


class CustomAdmin(admin.ModelAdmin):
    model = User

admin.site.register(User, CustomAdmin)