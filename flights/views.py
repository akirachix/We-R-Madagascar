from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import FlightRequest


class RequestFlightView(CreateView):
    model=FlightRequest
    form_class=RegisterclinicForm
    template_name='flight/request_flight.html'
    success_url=reverse_lazy('')
    

    def form_valid(self,form):
        return super (RequestFlightView,self).form_valid(form)

class PendingFlightRequestsListView(ListView):
    model = FlightRequest
    template = 'pending_request.html'

    def pending_requests(request):
        pending_flight_requests = FlightRequest.objects.all()
        pending_flight_requests_count = pending_requests.count()

        context={
            'pending_flight_requests ':pending_flight_requests,
            'pending_flight_requests_count':pending_flight_requests_count,
            }
        return render(request,context}

class DelayedFlightRequestsListView(ListView):
    model = FlightRequest
    template = 'delayed_request.html'

    def delayed_requests(request):
        delayed_flight_requests = FlightRequest.objects.filter(status="Delayed")
        delayed_flight_requests_count = delayed_flight_requests.count()

        context={
            'delayed_flight_requests':pending_requests ,
            'delayed_flight_requests_count':delayed_flight_requests_count,
        }
        return render(request,context}

class ScheduledFlightRequestsListView(ListView):
    model = FlightRequest
    template = 'scheduled_request.html'

    def scheduled_requests(request):
        scheduled_flight_requests = FlightRequest.objects.filter(status="Scheduled")
        scheduled_flight_requests_count = scheduled_flight_requests.count()

        context = {
            'scheduled_flight_requests':scheduled_flight_requests,
            'scheduled_flight_requests_count':scheduled_flight_requests_count,
        }
        return render(request,context)


