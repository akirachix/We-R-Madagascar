from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView
from django.shortcuts import render
from .models import FlightRequest
from .forms import RequestFlightForm
from django.urls import reverse_lazy
from .models import *
from django.core.paginator import InvalidPage,Paginator

def request_flight(request):
    flight_form = RequestFlightForm()
    if request.method == 'POST':
        flight_form = RequestFlightForm(request.POST or None)
        print("error")
        if flight_form.is_valid():
            flight_request = flight_form.save(commit=False)
            flight_request.user = request.user
            flight_request.save()
            return redirect('/pending-flights/')
        else:
            print(flight_form.errors.as_data())

    flight_form = RequestFlightForm()
    
    return render(request,'flight/request_flight.html', {'flight_form':flight_form})

class PendingRequestsView(ListView):
    model=FlightRequest
    template_name='flight/pending_flights.html'
    context_object_name="requested_flights"


    def get(self, request, *args,**kwargs):
        pending_flights=FlightRequest.objects.all()
        paginator=Paginator(pending_flights,30)
        is_paginated=True if paginator.num_pages > 1 else False
        page=request.GET.get("page") or 1
        search_post = request.GET.get('search')
        try:
            current_page=paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context={"requested_flights":current_page,"is_paginated":is_paginated,"count": FlightRequest.objects.all().count()}
        return render(request,self.template_name,context)
 
def delayed_flights(request):
    delayed_flight_requests = FlightRequest.objects.filter(status="Delayed")
    delayed_flight_requests_count = delayed_flight_requests.count()
    context={
        'delayed_flight_requests':delayed_flight_requests,
        'delayed_flight_requests_count':delayed_flight_requests_count,
        }
    return render(request,"flight/delayed_flights.html",context)



def scheduled_requests(request):
    scheduled_flight_requests = FlightRequest.objects.filter(status="Scheduled")
    scheduled_flight_requests_count = scheduled_flight_requests.count()
    context = {
        'scheduled_flight_requests':scheduled_flight_requests,
        'scheduled_flight_requests_count':scheduled_flight_requests_count,
        }
    return render(request,"flight/scheduled_flights.html",context)


