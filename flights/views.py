from audioop import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView,CreateView
from django.shortcuts import render
import requests
from .models import FlightRequest
# from .forms import DelayedReasonForm, RequestFlightForm
from django.urls import reverse_lazy
from .models import *
from django.core.paginator import InvalidPage,Paginator
from django.db.models import Q

def request_flight(request):
    flight_form = RequestFlightForm()
    if request.method == 'POST':
        flight_form = RequestFlightForm(request.POST or None)
        print("error")
        if flight_form.is_valid():
            flight_request = flight_form.save(commit=False)
            flight_request.user = request.user
            flight_request.save()
            return redirect('pending_requests')
        else:
            print(flight_form.errors.as_data())

    flight_form = RequestFlightForm()
    
    return render(request,'flight/request_flight.html', {'flight_form':flight_form})


class PendingRequestsView(View):
    model=FlightRequest
    template_name='flight/pending_flights.html'
    def get(self, request, *args,**kwargs):
        response = requests.get('https://drone.psi-mg.org/index.php/Export_data_by_tags/get_planning/12019112715581748016523394084163128401_qsclxSDCEDQ2/Planning_de_vol')
        z=response.json()
        x=z.get('posts')
        print(x)
        for y in x:
            FlightRequest.objects.update_or_create(**y)
        pending_flights=FlightRequest.objects.all()
        paginator=Paginator(pending_flights,30)
        is_paginated=True if paginator.num_pages > 1 else False
        page=request.GET.get("page") or 1
        search_post = request.GET.get('search')
        if search_post:
            clinics = FlightRequest.objects.filter(Q(clinic_name__icontains=search_post) & Q(status__icontains="Pending"))
            if not clinics:
                message="Looks like the clinic doesn't exist. Try searching using the clinic name"
                return render(request,self.template_name,{'message':message,"requested_flights":pending_flights})
            results=clinics.count()
        else:
            return render (request,self.template_name,{"requested_flights":pending_flights})
        try:
            current_page=paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context={"requested_flights":current_page,"is_paginated":is_paginated,"count": FlightRequest.objects.all().count(),"results":results}
        return render(request,self.template_name,context)


class DelayedFlightsView(View):
    model=FlightRequest
    template_name='flight/delayed_flights.html'

    def get(self,request):
        delayed_flight_requests = FlightRequest.objects.filter(status="Delayed")
        delayed_flight_requests_count = delayed_flight_requests.count()
        search_post = request.GET.get('search')
        if search_post:
            clinics = FlightRequest.objects.filter(Q(clinic_name__icontains=search_post) & Q(status__icontains="Delayed"))
            if not clinics:
                
                context={
                    'delayed_flight_requests':delayed_flight_requests,
                    'delayed_flight_requests_count':delayed_flight_requests_count,
                    'message':"Looks like the clinic doesn't exist. Try searching using the clinic name"
                    }
                return render(request,self.template_name,context)
            results=clinics.count()
        else:
            context={
                    'delayed_flight_requests':delayed_flight_requests,
                    'delayed_flight_requests_count':delayed_flight_requests_count,
                    'results':results,
                    }
            return render(request,self.template_name,context)
        context={
                    'delayed_flight_requests':clinics,
                    'delayed_flight_requests_count':delayed_flight_requests_count,
                    'results':results,
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

class ScheduleRequestsView(View):
    model=FlightRequest
    template_name='flight/scheduled_flights.html'

    def get(self,request):
        scheduled_flight_requests = FlightRequest.objects.filter(status="Scheduled")
        scheduled_flight_requests_count = scheduled_flight_requests.count()
        search_post = request.GET.get('search')
        if search_post:
            clinics = FlightRequest.objects.filter(Q(clinic_name__icontains=search_post) & Q(status__icontains="Scheduled"))
            if not clinics:
                context = {
                    'scheduled_flight_requests':scheduled_flight_requests,
                    'scheduled_flight_requests_count':scheduled_flight_requests_count,
                    'message':"Looks like the clinic doesn't exist. Try searching using the clinic name"
                    }
                return render(request,self.template_name,context)
            results=clinics.count()
        else:
            context = {
                    'scheduled_flight_requests':scheduled_flight_requests,
                    'scheduled_flight_requests_count':scheduled_flight_requests_count,
                    }
            return render(request,self.template_name,context)
        context = {
                    'scheduled_flight_requests':clinics,
                    'scheduled_flight_requests_count':scheduled_flight_requests_count,
                    'results':results,
                    }
        return render(request,self.template_name,context)
    
    def post(self, request):
        id=request.POST.get('pk')
        scheduled_flight= FlightRequest.objects.get(id=id)
        print(scheduled_flight)
        scheduled_flight.status="Scheduled"
        scheduled_flight.save()
        return redirect("scheduled_requests")


