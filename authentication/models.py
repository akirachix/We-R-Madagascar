from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from ohio import settings


class User(AbstractUser):
    username = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)



class Role(models.Model):
    CLINIC = 1
    FLYING_LABS = 2
    MINISTRY = 3
    ADMIN = 4

    ROLE_CHOICES = (
        (CLINIC, 'clinic'),
        (FLYING_LABS, 'flying_labs'),
        (MINISTRY, 'ministry'),
        (ADMIN, 'admin')
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

        
    





