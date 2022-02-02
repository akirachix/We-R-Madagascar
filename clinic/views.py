import csv, io
from django.shortcuts import render
from django.contrib import messages
from .models import Clinic

def clinic_upload(request):
    # declaring the template
    template = "upload_clinics.html"
    data = Clinic.objects.all()

    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'Clinic': data    
              }

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')

    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Clinic.objects.update_or_create(
            name=column[0],
            email=column[1],
            address=column[2],
            profile=column[4]
        )
    context = {}
    return render(request, template, context)