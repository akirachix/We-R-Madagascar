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
import os
from decouple import config
import telerivet

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def webhook(request):
    print(request.POST.get('secret') )
    webhook_secret = '2K2ZFHR3QDCWM46PZ6AR2NAPM6ZC7MZZ'
    if request.POST.get('secret') != webhook_secret:
        print("hey Guys")
        return HttpResponse("Invalid webhook vd dcdd secret", 'text/plain', 403)
    if request.POST.get('event') == 'incoming_message':
        content = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')
        
        return HttpResponse(json.dumps({
            'messages': [
                {'content': "Thanks for your messagessss!"}
                ]
                }), 'application/json') 
    return("hello")

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
    shipments_list =Schedules.objects.all()
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