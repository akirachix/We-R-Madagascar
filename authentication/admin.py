from django.contrib import admin

# Register your models here.
from authentication.models import UserProfile, User
from django.contrib.auth.admin import UserAdmin


# class CustomAdmin(admin.ModelAdmin):
#     model = User

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)