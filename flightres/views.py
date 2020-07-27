import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.core import serializers
import requests
from django.contrib.auth import get_user

from .models import FlightPermission, Report
from registry.models import Aircraft, Operator


def homeView(request):
    return render(request, 'flightres/home.html')


@login_required
def dashboardView(request):
    return render(request, 'flightres/dashboard.html')


class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission
    queryset = FlightPermission.objects.all().order_by('-flight_start_date')
    template_name = 'flightres/flightpermission_list.html'
    

    def get_context_data(self, *args, **kwargs):
        com = super(FlightPermissionList, self).get_context_data(
            *args, **kwargs)
        data = FlightPermission.objects.values('uav_uid', 'uav_uuid__operator__company_name', 'uav_uuid__operator__phone_number',
                                               'uav_uuid__operator__email', 'flight_start_date', 'flight_end_date', 'flight_time', 'flight_purpose',
                                               'uav_uuid__popular_name', 'flight_insurance_url', 'pilot_id__name', 'pilot_id__phone_number',
                                               'pilot_id__cv_url', 'latitude', 'longitude', 'flight_plan_url', 'location', 'status'
                                               )
        json_data = json.dumps(list(data), cls=DjangoJSONEncoder)
        com['json_data'] = json_data
        return com


@login_required
def approvePerm(request, pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'approve':
        selected_perm.status = 'Approved'
    elif action == 'deny':
        selected_perm.status = 'Rejected'
    selected_perm.save()
    return redirect('/np/dashboard/permission')


def flightReqResponseView(request, pk):
    selected_flight = get_object_or_404(FlightPermission, uav_uid=pk)
    if selected_flight.status == 'Approved':
        return render(request, 'flightres/verified_pg.html', {'object': selected_flight})
    elif selected_flight.status == 'Rejected':
        return render(request, 'flightres/reject_pg.html', {'object': selected_flight})
    else:
        return render(request, 'flightres/pending_pg.html', {'object': selected_flight})


@login_required
def updateComplain(request, pk, action):
    selected_complain = get_object_or_404(Report, uav_uid=pk)
    if action == 'status':
        selected_complain.status = 'Resolved'
    elif action == 'escalate':
        selected_complain.is_escalated = True
    selected_complain.save()
    return redirect('/np/dashboard/complain')


@login_required
def submitReply(request, pk):
    selected_complain = get_object_or_404(Report, uav_uid=pk)
    selected_complain.note = request.POST.get('note')
    selected_complain.reply = request.POST.get('reply')
    selected_complain.save()
    return redirect('/np/dashboard/complain')


class ComplainListView(LoginRequiredMixin, ListView):
    template_name = 'flightres/complaint_management.html'
    model = Report


@login_required
def uploadSheet(request):
    if request.method == 'POST' and request.FILES['sheet']:
        name = request.POST.get('name')
        myfile = request.FILES['sheet']
        current_user = get_user(request)
        fs = FileSystemStorage()
        fs.location = "./uploads/sheet_uploads"
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        files = {
            'name': (None, name),
            'upload_sheet': ('./uploads/sheet_uploads/{}'.format(uploaded_file_url), open('./uploads/sheet_uploads/{}'.format(uploaded_file_url), 'rb')),
            # 'created_by': current_user
        }

        response = requests.post(
            'http://localhost:8000/np/api/v1/sheet-upload/', files=files)

    return redirect('/np/dashboard/permission')


class AboutPageView(TemplateView):
    template_name = 'flightres/about.html'


class GuidelinesPageView(TemplateView):
    template_name = 'flightres/guidelines.html'


class OperdatorDatabaseView(LoginRequiredMixin, ListView):
    template_name = 'flightres/operators_db.html'
    queryset = Aircraft.objects.all()
