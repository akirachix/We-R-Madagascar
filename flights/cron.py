from .models import FlightRequest # importing the test model

def my_scheduled_job():
  FlightRequest.objects.create(name='test')