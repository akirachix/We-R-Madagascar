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