from django.shortcuts import render, redirect
from .models import *
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy 
from django.views.generic.list import ListView
from .models import Schedule
from django.views.generic import CreateView
from .forms import ScheduleForm,DelayedForm,RescheduleForm
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

        return redirect ('shipments:shipment')
    context["form"] = form
    return render(request, "edit_shipment.html", context)
 

# def delayedShipmentsList(request):
#     delayedlist =Schedule.objects.all()
#     return render (request, 'delayed_shipments.html',{'delayedlist':delayedlist})
    

def checkDelayedShipments(request):
    shipments_list =Schedule.objects.filter(status = 'Delayed')
    return render(request,'delayed_shipments.html',{'shipments_list' : shipments_list })




def countScheduledShipments(request):
    shipments_count = Schedule.objects.all().count()
    return render(request,'shipment:shipment',{'shipments_count':shipments_count})
  

def edit_delay(request, id):
    context = {}

    reschedule= Schedule.objects.get( id = id)
    form =RescheduleForm(request.POST or None, instance = reschedule)


    if form.is_valid():
        form.save()

        return redirect ('shipments:delayed_shipments')
    context["form"] = form
    return render(request, "edit_delay.html", context)

def checkCompletedShipments(request):
    completed_list =Schedule.objects.filter(status = 'Completed')
    return render(request,'completed_shipments.html',{'completed_list' : completed_list })

def completed_profile(request, id):
    view_profile = Schedule.objects.filter(id =id,status = 'Completed')

    return render (request, 'completed_profile.html', {'view_profile': view_profile})