import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Clinic
from .forms import ClinicForm
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

def clinic_upload(request):
	template = 'clinic/upload_clinics.html'
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

	context = {
		
	}
	return render (request, template, context)

def clinic_display(request):
	template = 'clinic/view_clinics.html'
	
	context = {
		'clinics': Clinic.objects.all(),
		'count': Clinic.objects.all().count()
	}

	return render (request, template, context)

