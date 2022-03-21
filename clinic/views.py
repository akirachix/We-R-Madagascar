import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Clinic
from .forms import ClinicForm
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.core.paginator import InvalidPage,Paginator
from django.views.generic.list import ListView
from django.db.models import Q
from django.db import IntegrityError

def clinic_upload(request):
    template = 'clinic/upload_clinics.html'
    try:

        prompt = {
'order': 'order of csv should be name, email, address, profile'
}
        if request.method == "GET":
            return render(request, template, prompt)

        csv_file = request.FILES["file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request,'This is not a csv file')

        data_set = csv_file.read().decode("UTF-8")	
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Clinic.objects.update_or_create(
            name = column[0],
            email = column[1],
            address = column[2],
            profile = column[3]
            )
    except IntegrityError as e:
        return render (request, 'clinic/error.html')

    context = {
}
    return redirect ("view_clinics")

class ClinicViewDetails(ListView):
    model=Clinic
    template_name='clinic/view_clinics.html'
    context_object_name="clinics"


    def get(self, request, *args,**kwargs):
        clinics=Clinic.objects.all()
        paginator=Paginator(clinics,30)
        is_paginated=True if paginator.num_pages > 1 else False
        page=request.GET.get("page") or 1
        search_post = request.GET.get('search')
        try:
            current_page=paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context={"clinics":current_page,"is_paginated":is_paginated,"count": Clinic.objects.all().count()}
        return render(request,self.template_name,context)

def search_clinic(request):
    search_post = request.GET.get('search')
    if search_post:
        clinics = Clinic.objects.filter(Q(name__icontains=search_post))
        results=clinics.count()
    else:
        clinics = Clinic.objects.all()
        message="Looks like the clinic doesn't exist. Try searching using the clinic name"
        return render (request,'clinic/view_clinics.html',{'clinics':clinics,'message':message})
    return render (request,'clinic/view_clinics.html',{'clinics': clinics,'results':results})

