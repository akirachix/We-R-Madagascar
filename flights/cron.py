from .models import FlightRequest
from ohio.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def scheduled_job():
    all_flights=FlightRequest.objects.filter(status='Scheduled')
    if all_flights:
        emails="shadyaobuyagard@gmail.com"
        subject = "Cron Job Configuration"
        message = f"{all_flights.count()} Flights have been Scheduled"
        recipient=emails
        send_mail(subject, message,EMAIL_HOST_USER,[recipient])
    else:
        emails="shadyaobuyagard@gmail.com"
        subject = "Cron Job Configuration"
        message = f"Failure"
        recipient=emails
        send_mail(subject, message,EMAIL_HOST_USER,[recipient])


 