import csv, io
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Clinic
from .forms import ClinicForm
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
def clinic_upload(request):
   
    template = "clinic/upload_clinics.html"
    clinic_data = Clinic.objects.all()
    try:
# prompt is a context variable that can have different values      depending on their context
        prompt = {
            'order': 'Order of the CSV should be name,email,address, profile',
            'profiles': clinic_data
                }
        # GET request returns the value of the data with the specified key.
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES.get('file')
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        clinic_data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(clinic_data_set)
        next(io_string)
        

        clinic_csvf = csv.reader(io_string, delimiter=',', quotechar="|")
        clinic_data = []
        for name,email,address,profile, *__ in clinic_csvf:
            Clinic.objects.update_or_create(
                name=name,
                email=email,
                address=address,
                profile=profile
            )
        

    except Exception as e: 
        print(e)
        return render(request,"clinic/error.html",{'e':e})

    context = {}
    return render(request, template, context)


def clinic_display(request):
    template = 'clinic/view_clinics.html'
    
    context = {
        'clinics': Clinic.objects.all(),
        'count': Clinic.objects.all().count()
    }

    return render (request, template, context)

def search_clinic(request):
    search_post = request.GET.get('search')
    all_clinics = Clinic.objects.all()
    print(search_post)
    if search_post:
        clinics = Clinic.objects.filter(Q(name__icontains=search_post))
        if not clinics:
            message="Looks like the clinic doesn't exist. Try searching using the clinic name"
            return render (request,'clinic/view_clinics.html',{'clinics':all_clinics,'message':message})
        
        results=clinics.count()
    else:
        
        return render (request,'clinic/view_clinics.html',{'clinics':all_clinics,'message':message})
    return render (request,'clinic/view_clinics.html',{'clinics': clinics,'results':results})