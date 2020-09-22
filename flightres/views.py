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
import decimal
import json
import requests
from django.contrib.auth import get_user
import datetime

from .models import FlightPermission, Report, LocalAuthorities
from registry.models import Aircraft, Operator


def homeView(request):
    return render(request, 'flightres/home.html')


@login_required
def dashboardView(request):
    # data for cards on top of the dashboard page
    top_row_data = []
    drone_op_num = Operator.objects.all().count()
    drone_num = Aircraft.objects.all().count()
    complaint_num = Report.objects.all().count()
    solved_complaints = Report.objects.filter(status='Resolved').count()
    pending_complaints = Report.objects.filter(status='Pending').count()
    top_row_data.append([drone_op_num, drone_num, complaint_num,
                         solved_complaints, pending_complaints])

    # data for pie chart
    pie_data = []
    pie_data.append([solved_complaints, pending_complaints])

    day_delta = datetime.timedelta(days=30)
    start_date = datetime.date(datetime.date.today().year, 1, 1)
    end_date = datetime.date(datetime.date.today().year, 12, 30)
    barchart_data = []
    for i in range(12):
        getDay = (start_date + i * day_delta)
        getEndday = getDay + datetime.timedelta(days=30)
        # data for bar chart
        total_requests = FlightPermission.objects.filter(
            created_date__gt=getDay, created_date__lt=getEndday).count()
        approved_requests = FlightPermission.objects.filter(
            status='Approved', created_date__gt=getDay, created_date__lt=getEndday).count()
        barchart_data.append([total_requests, approved_requests])
    return render(request, 'flightres/dashboard.html',
                  {'top_data': top_row_data, 'bar_data': barchart_data, 'pie_data': pie_data})


class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission
    ordering = 'uav_uid'
    template_name = 'flightres/flightpermission_list.html'

    # def get_queryset(self, *args, **kwargs) :
    #     type = self.kwargs['type']
    #     if type == 'special':
    #         queryset = FlightPermission.objects.filter(is_special_permission=True).order_by('-flight_start_date')
    #     elif type == 'general':
    #         queryset = FlightPermission.objects.filter(is_special_permission=False).order_by('-flight_start_date')
    #     else:
    #         queryset = None
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        com = super(FlightPermissionList, self).get_context_data(
            *args, **kwargs)
        raw_data = FlightPermission.objects.values('uav_uid', 'uav_uuid', 'uav_uuid__operator__company_name',
                                                   'uav_uuid__operator__phone_number',
                                                   'uav_uuid__operator__email', 'flight_start_date', 'flight_end_date',
                                                   'flight_time', 'flight_purpose',
                                                   'uav_uuid__popular_name', 'flight_insurance_url', 'pilot_id__name',
                                                   'pilot_id__phone_number', 'pilot_id__company',
                                                   'pilot_id__cv_url', 'latitude', 'longitude', 'flight_plan_url',
                                                   'location', 'status'
                                                   ).order_by('-uav_uid')
        json_data = json.dumps(list(raw_data), cls=DjangoJSONEncoder)
        com['json_data'] = json_data
        object_data = []
        type = self.kwargs['type']
        if type == 'special':
            com['title'] = 'SPECIAL FLIGHT'
            flight_objects = FlightPermission.objects.filter(
                is_special_permission=True).order_by('-uav_uid')
        elif type == 'general':
            com['title'] = 'FLIGHT'
            flight_objects = FlightPermission.objects.filter(
                is_special_permission=False).order_by('-uav_uid')
        else:
            flight_objects = FlightPermission.objects.filter(
                is_special_permission=False).order_by('-uav_uid')
        for flight_object in flight_objects:
            due = flight_object.flight_start_date - datetime.date.today()
            due_in = due.days
            object_data.append([flight_object, due_in])
        com['object_data'] = object_data
        return com


@login_required
def approvePerm(request, pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'approve':
        selected_perm.status = 'Approved'
    elif action == 'deny':
        selected_perm.status = 'Rejected'
    selected_perm.save()
    # prev_url = str(request.META.get('HTTP_REFERER'))
    # url = prev_url.split("np")[1]
    if selected_perm.is_special_permission == True:
        return redirect('/np/dashboard/permission/special')
    else:
        return redirect('/np/dashboard/permission/general')


@login_required
def denyPerm(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        # print(data['value'], "here")
        selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
        selected_perm.status = 'Rejected'
        selected_perm.rejection_reason = data['value']
        selected_perm.save()
        if selected_perm.is_special_permission == True:
            return redirect('/np/dashboard/permission/special')
        else:
            return redirect('/np/dashboard/permission/general')


def flightReqResponseView(request, pk):
    selected_flight = get_object_or_404(FlightPermission, uav_uid=pk)
    if selected_flight.status == 'Approved':
        return render(request, 'flightres/verified_pg.html', {'object': selected_flight})
    elif selected_flight.status == 'Rejected':
        return render(request, 'flightres/reject_pg.html', {'object': selected_flight})
    else:
        return render(request, 'flightres/pending_pg.html', {'object': selected_flight})


@login_required
def updateComplain(request, pk, action, status):
    selected_complain = get_object_or_404(Report, uav_uid=pk)
    if action == 'status':
        if status == "Pending":
            selected_complain.status = 'Resolved'
        elif status == "Resolved":
            selected_complain.status = 'Pending'
    elif action == 'escalate':
        if status == 'true':
            selected_complain.is_escalated = False
        elif status == 'false':
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
    ordering = '-uav_uid'

    def get_context_data(self, *args, **kwargs):
        com = super(ComplainListView, self).get_context_data(
            *args, **kwargs)
        complains = Report.objects.all().order_by('-uav_uid')
        data = []
        for complain in complains:
            nearby = None
            nearby_auth = None
            this_lat = complain.latitude
            this_lon = complain.longitude
            lower_lat = this_lat - decimal.Decimal(0.090)
            upper_lat = this_lat + decimal.Decimal(0.090)
            lower_lon = this_lon - decimal.Decimal(0.090)
            upper_lon = this_lon + decimal.Decimal(0.090)
            # print(lower_lat, upper_lat, lower_lon, upper_lon)
            nearby = FlightPermission.objects.filter(latitude__lte=upper_lat,
                                                     latitude__gte=lower_lat,
                                                     longitude__lte=upper_lon,
                                                     longitude__gte=lower_lon)[:4]
            nearby_auth = LocalAuthorities.objects.filter(latitude__lte=upper_lat,
                                                          latitude__gte=lower_lat,
                                                          longitude__lte=upper_lon,
                                                          longitude__gte=lower_lon)[:4]
            data.append([complain, nearby, nearby_auth])
        com['data'] = data
        flight_objects = FlightPermission.objects.values('uav_uid', 'uav_uuid__operator__company_name', 'uav_uuid', 'uav_uuid__operator__phone_number',
                                                         'uav_uuid__operator__email', 'flight_start_date', 'flight_end_date', 'flight_time', 'flight_purpose',
                                                         'uav_uuid__popular_name', 'flight_insurance_url', 'pilot_id__name', 'pilot_id__phone_number', 'pilot_id__company',
                                                         'pilot_id__cv_url', 'latitude', 'longitude', 'flight_plan_url', 'location', 'status'
                                                         ).order_by('-uav_uid')
        image_urls = Report.objects.values('uav_uid', 'image_url')
        image_json_data = json.dumps(list(image_urls), cls=DjangoJSONEncoder)
        json_data = json.dumps(list(flight_objects), cls=DjangoJSONEncoder)
        com['json_data'] = json_data
        com['image_json_data'] = image_json_data
        # print(data)
        return com


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
            'upload_sheet': ('./uploads/sheet_uploads/{}'.format(uploaded_file_url),
                             open('./uploads/sheet_uploads/{}'.format(uploaded_file_url), 'rb')),
            'created_by': current_user.id
        }

        response = requests.post(
            'http://localhost:8000/np/api/v1/sheet-upload/', files=files)
        res_json = response.json()
        print(response, res_json['message'])
    return redirect('/np/dashboard/operators')


class AboutPageView(TemplateView):
    template_name = 'flightres/about.html'


class GuidelinesPageView(TemplateView):
    template_name = 'flightres/guidelines.html'


class OperdatorDatabaseView(LoginRequiredMixin, ListView):
    template_name = 'flightres/operators_db.html'
    queryset = Aircraft.objects.all().order_by('-unid')


def view_404(request, exception):
    '''
    This if for custom 404 template
    '''
    return render(request, 'flightres/404.html')


def view_500(request):
    '''
    This if for custom 500 template
    '''
    return render(request, 'flightres/404.html')
