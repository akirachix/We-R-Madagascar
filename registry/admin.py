from django.contrib import admin
from .models import Authorization, Activity, Operator, Contact, Aircraft, Person, Address, Pilot, Complain

# Register your models here.

admin.site.register(Authorization)
admin.site.register(Activity)
admin.site.register(Operator)
admin.site.register(Contact)
admin.site.register(Aircraft)
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Pilot)
admin.site.register(Complain)
