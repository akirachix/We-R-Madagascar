from django.shortcuts import render, redirect
from .models import *
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy 
from django.views.generic.list import ListView
from .models import Schedules
from django.views.generic import CreateView
# from .forms import ScheduleForm,DelayedForm,RescheduleForm
from . import views
import requests
import json

# Create your views here.
       
# class ScheduleFormView(CreateView):
#     form_class = ScheduleForm
#     model = Schedules
#     template_name = 'schedule.html'
#     success_url = reverse_lazy('shipment:shipment')


def scheduledShipmentsList(request):
    response = requests.get('https://drone.psi-mg.org/index.php/Export_data_by_tags/get_quantification_produit/12019112715581748016523394084163128401_qsclxSDCEDQ3/Quantification_produit')
    z=response.json()
    x=z.get('posts')
    for y in x:
        Schedules.objects.update_or_create(**y)
   

    mylist=Schedules.objects.all()
    schedule_count = mylist.count()
    return render(request,'scheduled_shipments.html',{'mylist':mylist,'schedule_count':schedule_count}
)

def edit_shipment(request, id):
    context = {}

    delayed= Schedules.objects.get( id = id)
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
    shipments_list =Schedules.objects.filter(status = 'Delayed')
    delayed_count = shipments_list.count()
    return render(request,'delayed_shipments.html',{'shipments_list' : shipments_list ,'delayed_count':delayed_count})



def edit_delay(request, id):
    context = {}

    reschedule= Schedules.objects.get( id = id)
    form =RescheduleForm(request.POST or None, instance = reschedule)


    if form.is_valid():
        form.save()

        return redirect ('shipments:delayed_shipments')
    context["form"] = form
    return render(request, "edit_delay.html", context)

def checkCompletedShipments(request):
    completed_list =Schedules.objects.filter(status = 'Completed')
    completed_count = completed_list.count()
    return render(request,'completed_shipments.html',{'completed_list' : completed_list,'completed_count':completed_count })

def completed_profile(request, id):
    view_profile = Schedules.objects.filter(id =id,status = 'Completed')

    return render (request, 'completed_profile.html', {'view_profile': view_profile})