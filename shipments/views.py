from django.shortcuts import render, redirect
from .models import *
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy 
from django.views.generic.list import ListView
from .models import Schedule
from .forms import ScheduleForm,DelayedForm,RescheduleForm
from . import views
from django.db.models import Q


# Create your views here.
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
def update(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)

        if form.is_valid():
            print("schedule form is valid")
            form.save()
            return redirect("shipments:shipment")
        else:
            print("ERROR : ", form.errors)
    else:
        form = ScheduleForm()

    template_name = "schedule.html"
    context = {
        "form":form,
    }

    return render(request, template_name, context)
def scheduledShipmentsList(request):

    mylist=Schedule.objects.all()
    schedule_count = mylist.count()
    return render(request,'scheduled_shipments.html',{'mylist':mylist,'schedule_count':schedule_count}
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
    delayed_count = shipments_list.count()
    return render(request,'delayed_shipments.html',{'shipments_list' : shipments_list ,'delayed_count':delayed_count})



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
    completed_count = completed_list.count()
    return render(request,'completed_shipments.html',{'completed_list' : completed_list,'completed_count':completed_count })

def completed_profile(request, id):
    view_profile = Schedule.objects.filter(id =id,status = 'Completed')

    return render (request, 'completed_profile.html', {'view_profile': view_profile})



def search_clinic(request):
    search_post = request.GET.get('search')
    all_shipments = Schedule.objects.all()
    print(search_post)
    if search_post:
        shipments = Schedule.objects.filter(Q(shipment_id__icontains=search_post))
        if not shipments:
            message="Looks like the clinic doesn't exist. Try searching using the clinic name"
            return render (request,'scheduled_shipments.html',{'shipments': all_shipments,'message':message})
        
        results=shipments.count()
    else:
        
        return render (request,'scheduled_shipments.html',{'shipments': all_shipments,'message':message})
    return render (request,'scheduled_shipments.html',{'shipments': shipments,'results':results})