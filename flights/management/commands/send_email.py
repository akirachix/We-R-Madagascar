from django.core.management.base import BaseCommand
from django.utils import timezone
from ohio.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from flights.models import FlightRequest

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_flights=FlightRequest.objects.filter(status='Scheduled')
        if all_flights:
            emails="shadyaobuyagard@gmail.com"
            subject = "Cron Job Configuration"
            message = f"{all_flights.count()} Flights have been Scheduled"
            recipient=emails
            send_mail(subject, message,EMAIL_HOST_USER,[recipient])
            print("Wated Youth")
        else:
            emails="shadyaobuyagard@gmail.com"
            subject = "Cron Job Configuration"
            message = f"Failure"
            recipient=emails
            send_mail(subject, message,EMAIL_HOST_USER,[recipient])
            print("Wasted Youth Fletcher")