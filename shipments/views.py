from django.shortcuts import render, redirect
from .models import *
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy 
from django.views.generic.list import ListView
from .models import Schedule, Delayed
from django.views.generic import CreateView
from .forms import ScheduleForm, DelayedForm
from . import views

# Create your views here.
       
class ScheduleFormView(CreateView):
    form_class = ScheduleForm
    model = Schedule
    template_name = 'schedule.html'
    success_url = reverse_lazy('shipment:shipment')


def scheduledShipmentsList(request):
    mylist=Schedule.objects.all()
    return render(request,'scheduled_shipments.html',{'mylist':mylist}
)

def edit_shipment(request, id):
    context = {}

    delayed= Schedule.objects.get( id = id)
    form =DelayedForm(request.POST or None, instance = delayed)


    if form.is_valid():
        form.save()

        return redirect ('shipments:delayed_shipments')
    context["form"] = form

    return render(request, "edit_shipment.html", context)

def delayedShipmentsList(request):
    delayedlist = Delayed.objects.all()
    return render (request, 'delayed_shipments.html',{'delayedlist':delayedlist})
