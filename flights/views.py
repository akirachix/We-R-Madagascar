from audioop import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView,CreateView
from django.shortcuts import render
from .models import FlightRequest
from .forms import DelayedReasonForm, RequestFlightForm
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


class PendingRequestsView(View):
    model=FlightRequest
    template_name='flight/pending_flights.html'
    def post(self, request,id):
        flight=FlightRequest.objects.get(id=id)
        form = DelayedReasonForm(request.POST,instance=flight)
        if form.is_valid():
            form.save()
            return redirect(reverse('delayed_requests'))
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args,**kwargs):
        pending_flights=FlightRequest.objects.all().filter(status="Pending")
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


class DelayedFlightsView(View):
    model=FlightRequest
    template_name='flight/delayed_flights.html'

    def get(self,request):
        delayed_flight_requests = FlightRequest.objects.filter(status="Delayed")
        delayed_flight_requests_count = delayed_flight_requests.count()
        context={
            'delayed_flight_requests':delayed_flight_requests,
            'delayed_flight_requests_count':delayed_flight_requests_count,
            }
        return render(request,self.template_name,context)
        
    def post(self, request):
        id=request.POST.get('pk')
        reason=request.POST.get('reason')
        print(reason)
        print(id)
        delayed_flight= FlightRequest.objects.get(id=id)
        delayed_flight.status="Delayed"
        delayed_flight.delayed_reasons=reason
        delayed_flight.save()
        return redirect('delayed_requests')


def modals(request,id):
    requested_flights=FlightRequest.objects.all()
    template_name='flight/pending_flights.html'
    flight=FlightRequest.objects.get(id=id)
    delayed_reason_form = DelayedReasonForm()
    if request.method == 'POST':
        delayed_reason_form = DelayedReasonForm(request.POST,instance=flight)
        print("error")
        if delayed_reason_form.is_valid():
            delayed_reason_form.save()
            return redirect(reverse('delayed_requests'))
        else:
            delayed_reason_form = DelayedReasonForm(instance=flight)
            print(delayed_reason_form.errors.as_data())
    context={
        "requested_flights":requested_flights,
        'delayed_reason_form':delayed_reason_form
    }
    return render(request,template_name,context)




class ScheduleRequestsView(View):
    model=FlightRequest
    template_name='flight/scheduled_flights.html'

    def get(self,request):
        scheduled_flight_requests = FlightRequest.objects.filter(status="Scheduled")
        scheduled_flight_requests_count = scheduled_flight_requests.count()
        context = {
            'scheduled_flight_requests':scheduled_flight_requests,
            'scheduled_flight_requests_count':scheduled_flight_requests_count,
            }
        return render(request,self.template_name,context)
    
    def post(self, request):
        id=request.POST.get('pk')
        

        scheduled_flight= FlightRequest.objects.get(id=id)
        print(scheduled_flight)
        scheduled_flight.status="Scheduled"
        scheduled_flight.save()
        return redirect("scheduled_requests")


