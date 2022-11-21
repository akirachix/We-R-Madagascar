from django.core.management.base import BaseCommand,CommandError
from flights.models import FlightRequest
from django.db.models import Q
import datetime

import telerivet
class Command(BaseCommand):
    help ="Sends SMS after every one minute"
    def handle(self,*args,**options):
        self.stdout.write(self.style.NOTICE("Checking Database for any changes....."))
        # Test.objects.create(name='test')
        try:
            date=datetime.datetime.now()
            two_mins_ago=date - datetime.timedelta(minutes=10)
            tr = telerivet.API('3Z65O_fsREJmv35duc6Vr1qCbJmxZj9fRNEM')
            project = tr.initProjectById('PJ514b358dbf7e0208')
            pending= FlightRequest.objects.filter(
                Q(status='Pending') & Q(last_updated__lte=date) & Q(last_updated__gte=two_mins_ago)
                )
            completed=FlightRequest.objects.filter(
                Q(status='Completed') & Q(last_updated__lte=date) & Q(last_updated__gte=two_mins_ago)
                )
            delayed=FlightRequest.objects.filter(
                Q(status='Delayed') & Q(last_updated__lte=date) & Q(last_updated__gte=two_mins_ago)
                )
            processed=FlightRequest.objects.filter(Q(status='Processed')& Q(last_updated__lte=date) & Q(last_updated__gte=two_mins_ago))
            dispatched=FlightRequest.objects.filter(Q(status='Dispatched')& Q(last_updated__lte=date) & Q(last_updated__gte=two_mins_ago))
            if pending:
                for flight in pending:
                    sent_msg = project.sendMessage(content =f"Hey {flight.clinic_name}, Your shipment has a status of {flight.status}", 
                    to_number = f"{flight.clinic_name.contact}")
            if completed:
                for flight in completed:
                    sent_msg = project.sendMessage(content =f"Hey {flight.clinic_name}, Your shipment has a status of {flight.status}", 
                    to_number = f"{flight.clinic_name.contact}")
            if delayed:
                for flight in delayed:
                    sent_msg = project.sendMessage(content =f"Hey {flight.clinic_name}, Your shipment has a status of {flight.status}", 
                    to_number = f"{flight.clinic_name.contact}")
            if processed:
                for flight in processed:
                    sent_msg = project.sendMessage(content =f"Hey {flight.clinic_name}, Your shipment has a status of {flight.status}", 
                    to_number = f"{flight.clinic_name.contact}")
            if dispatched:
                for flight in dispatched:
                    sent_msg = project.sendMessage(content =f"Hey {flight.clinic_name}, Your shipment has a status of {flight.status}", 
                    to_number = f"{flight.clinic_name.contact}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred....{e}'))



        