import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.core import serializers
import decimal
import pandas as pd
#import geopandas
from django.core.exceptions import ObjectDoesNotExist
import json
import requests
from django.contrib.auth import get_user
import datetime
from datetime import date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.serializers import serialize
from .models import FlightPermission, Report, LocalAuthorities, NoFlyZone
from registry.models import Aircraft, Operator, Manufacturer, Address
from django.contrib.messages.views import SuccessMessageMixin
from .form import AircraftForm, OperatorForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from zipfile import ZipFile


def homeView(request):
    return render(request, 'flightres/home.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/accounts/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'flightres/changepassword.html', {
        'form': form
    })


@login_required
def dashboardView(request):
    # data for cards on top of the dashboard page
    top_row_data = []
    drone_op_num = Operator.objects.all().count()
    drone_num = Aircraft.objects.all().count()
    complaint_num = Report.objects.all().count()
    solved_complaints = Report.objects.filter(status='Resolved').count()
    pending_complaints = Report.objects.filter(status='Pending').count()
    approved_requests_num = FlightPermission.objects.filter(status="Approved").count()
    pending_requests_num = FlightPermission.objects.filter(status="Pending").count()
    rejected_requests_num = FlightPermission.objects.filter(status="Rejected").count()
    top_row_data.append([drone_op_num, drone_num, approved_requests_num,
                         pending_requests_num, rejected_requests_num])
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


class FlightView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        object_list = FlightPermission.objects.all()
        shp_files = NoFlyZone.objects.all()
        shp_names = []
        count = -1
        for x in shp_files:
            count += 1
            if str(x.spatialdata_zip_file).endswith('.zip'):
                zipped = ZipFile(x.spatialdata_zip_file, 'r')
                for y in zipped.namelist():
                    if y.endswith('.shp'):
                        shp_names.append(y.replace('.shp', '.geojson'))
        context = {
            "object_list": object_list,
            'obj': json.dumps(list(shp_names), cls=DjangoJSONEncoder)

        }
        return render(request, 'flightres/map.html', context)

    def post(self, request, *args, **kwargs):
        start_date = request.POST['flight_start_date']
        end_date = request.POST['flight_end_date']
        flt_status = [
            request.POST.get('flt_approved', None),
            request.POST.get('flt_pending', None),
            request.POST.get('flt_rejected', None)
        ]
        comp_status = [
            request.POST.get('comp_pending', None),
            request.POST.get('comp_resolved', None)
        ]
        data3 = []
        datasuccess = []
        counts = 0
        
        data_rep = []
        data_rep_success = []
        rep_count = 0
        
        report_data = Report.objects.all()
        object_list = FlightPermission.objects.all()
        for data in object_list:
            if start_date or end_date != '' :
                if data.flight_start_date <= datetime.datetime.strptime(start_date,
                                                                        '%Y-%m-%d').date() <= data.flight_end_date or data.flight_end_date >= datetime.datetime.strptime(
                    end_date, '%Y-%m-%d').date() >= data.flight_start_date or (
                        data.flight_start_date >= datetime.datetime.strptime(start_date,
                                                                            '%Y-%m-%d').date() and data.flight_end_date <= datetime.datetime.strptime(
                    end_date, '%Y-%m-%d').date()):
                    #print(report_data)
                    if flt_status[0] == flt_status[1] == flt_status[2] == None:                      
                        data3.append(data)
                        counts += 1
                        datasuccess.append(counts)
                    else:
                        for x in flt_status:
                            
                            if x is not None:
                                if data.status == x:
                                    data3.append(data)
                                    counts += 1
                                    datasuccess.append(counts)
            else:
                if flt_status[0] or flt_status[1] or flt_status[2] is not None:
                    for x in flt_status:
                        if x is not None:
                            if data.status == x:
                                data3.append(data)
                                counts += 1
                                datasuccess.append(counts)
                
        if comp_status[0] or comp_status[1] is not None:
            for dat in report_data:
                for x in comp_status:
                    if dat.status == x:
                        data_rep.append(dat)
                        rep_count += 1
                        data_rep_success.append(rep_count)


        if datasuccess is not None or data_rep_success is not None:
            '''if (len(datasuccess) + len(data_rep_success)) > 1:
                msg = str(len(datasuccess) + len(data_rep_success)) + ' Flights were found'
            elif (len(datasuccess) + len(data_rep_success)) == 1:
                msg = str(len(datasuccess) + len(data_rep_success)) + ' Flight was found'
            else:
                object_list = ""
                msg = 'No Flight Found'

            messages.success(request, msg)'''
            

            context = {
                'flight_start_date': start_date,
                'flight_end_date': end_date,
                'flight_approved': False if flt_status[0] is None else True,
                'flight_pending': False if flt_status[1] is None else True,
                'flight_rejected': False if flt_status[2] is None else True,
                'complaint_pending': False if comp_status[0] is None else True,
                'complaint_resolved': False if comp_status[1] is None else True,
                "data3": '' if not data3 else data3,
                'data_rep': '' if not data_rep else data_rep

            }
            
        else:
            #messages.error(request, 'No matched Found')
            context = {
                'flight_start_date': start_date,
                'flight_end_date': end_date,
                'flight_approved': False if flt_status[0] is None else True,
                'flight_pending': False if flt_status[1] is None else True,
                'flight_rejected': False if flt_status[2] is None else True,
                'complaint_pending': False if comp_status[0] is None else True,
                'complaint_resolved': False if comp_status[1] is None else True,
                "object_list": object_list

            }

        return render(request, 'flightres/map.html', context)


class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission
    ordering = 'uav_uid'
    template_name = 'flightres/flightpermission_list.html'

    def get_context_data(self, *args, **kwargs):
        com = super(FlightPermissionList, self).get_context_data(
            *args, **kwargs)
        raw_data = FlightPermission.objects.values('uav_uid', 'uav_uuid', 'uav_uuid__operator__company_name',
                                                   'uav_uuid__operator__phone_number',
                                                   'uav_uuid__operator__email', 'flight_start_date', 'flight_end_date',
                                                   'flight_time', 'flight_purpose', 'rejection_reason', 'altitude',
                                                   'uav_uuid__popular_name', 'flight_insurance_url', 'pilot_id__name',
                                                   'pilot_id__phone_number', 'pilot_id__company',
                                                   'pilot_id__cv_url', 'latitude', 'longitude', 'flight_plan_url',
                                                   'location', 'status', 'assigned_to__username', 'assigned_to__email'
                                                   ).order_by('-uav_uid')
        json_data = json.dumps(list(raw_data), cls=DjangoJSONEncoder)
        com['json_data'] = json_data
        com['current_user'] = self.request.user.username
        com['current_user_email'] = self.request.user.email
        object_data = []
        perm_type = self.kwargs['type']
        if perm_type == 'special':
            com['title'] = 'SPECIAL FLIGHT'
            flight_objects = FlightPermission.objects.filter(
                is_special_permission=True).order_by('-uav_uid')
        elif perm_type == 'general':
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


@login_required
def assignPerm(request, pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'assign':
        selected_perm.assigned_to = request.user
    elif action == 'unassign':
        selected_perm.assigned_to = None
    selected_perm.save()
    if selected_perm:
        if action == 'assign':
            resp1 = {
                'result': request.user.username,
                'assigned_to__email': selected_perm.assigned_to.email,
                'assigned_to__username': selected_perm.assigned_to.username,
                'latitude': selected_perm.latitude,
                'longitude': selected_perm.longitude
            }
            return JsonResponse(resp1)
        elif action == 'unassign':
            resp2 = {
                'result': None,
                'assigned_to__email': None,
                'assigned_to__username': None,
                'latitude': selected_perm.latitude,
                'longitude': selected_perm.longitude
            }
            return JsonResponse(resp2)
        else:
            resp4 = {
                'result': 'Invalid Url'
            }
            return JsonResponse(resp4)


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
        nearby_flight = []
        nearby_auth_flight = []
        for complain in complains:
            nearby = None
            nearby_auth = None
            this_lat = complain.latitude
            this_lon = complain.longitude
            lower_lat = this_lat - decimal.Decimal(0.180)
            upper_lat = this_lat + decimal.Decimal(0.180)
            lower_lon = this_lon - decimal.Decimal(0.180)
            upper_lon = this_lon + decimal.Decimal(0.180)
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
            for x in nearby:
                if x.flight_start_date <= complain.created_at.date() <= x.flight_end_date:
                    nearby_flight.append([complain.uav_uid, x.latitude, x.longitude, x.uav_uid, x.altitude, x.status])
            for x in nearby_auth:
                nearby_auth_flight.append([complain.uav_uid, x.latitude, x.longitude, x.name, x.phone_number])
        com['data'] = data
        com['nearby_flt'] = json.dumps(list(nearby_flight), cls=DjangoJSONEncoder)
        com['nearby_auth_flt'] = json.dumps(list(nearby_auth_flight), cls=DjangoJSONEncoder)

        flight_objects = FlightPermission.objects.values('uav_uid', 'uav_uuid__operator__company_name', 'uav_uuid',
                                                         'uav_uuid__operator__phone_number',
                                                         'uav_uuid__operator__email', 'flight_start_date',
                                                         'flight_end_date', 'flight_time', 'flight_purpose',
                                                         'rejection_reason',
                                                         'uav_uuid__popular_name', 'flight_insurance_url',
                                                         'pilot_id__name', 'pilot_id__phone_number',
                                                         'pilot_id__company',
                                                         'pilot_id__cv_url', 'latitude', 'longitude', 'flight_plan_url',
                                                         'location', 'status', 'assigned_to'
                                                         ).order_by('-uav_uid')
        image_urls = Report.objects.values('uav_uid', 'image_url')
        image_json_data = json.dumps(list(image_urls), cls=DjangoJSONEncoder)
        json_data = json.dumps(list(flight_objects), cls=DjangoJSONEncoder)
        com['json_data'] = json_data
        com['image_json_data'] = image_json_data
        # print(data)
        return com


'''
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
        # print(response, res_json['message'])
    return redirect('/np/dashboard/operators')
    '''


@login_required()
def bulkupload(request):
    template = 'operators_db.html'

    # prompt = {
    #     'order': '''1. Please upload a .csv or .xls file \n
    #                 2. Order of the file columns should be Province, District, Municipality, Partner, Branch, No. of Tablets'''
    # }

    if request.method == "GET":
        return render(request, template)

    if request.method == 'POST':
        uploaded_file = request.FILES['sheet']

        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file).fillna('')
            except UnboundLocalError as error:
                messages.WARNING(request, 'Invalid File Uploaded')
                return redirect('/np/dashboard/operators', messages)
            except Exception as exception:
                messages.WARNING(request, 'Invalid File Uploaded')
                return redirect('/np/dashboard/operators', messages)
        elif uploaded_file.name.endswith(('.xls', 'xlsx')):
            try:
                df = pd.read_excel(uploaded_file).fillna('')
            except UnboundLocalError as error:
                messages.WARNING(request, 'Invalid File Uploaded')
                return redirect('/np/dashboard/operators', messages)
            except Exception as exception:
                messages.WARNING(request, 'Invalid File Uploaded')
                return redirect('/np/dashboard/operators', messages)
        else:
            messages.error(request, "Please upload a .csv or .xls file")

        upper_range = len(df)

        success_count = 0
        for row in range(0, upper_range):
            try:
                manufacturer = None if df['UAV Manufacturer & Model'][row] == '' else df['UAV Manufacturer & Model'][
                    row]
                address = None if df['Address'][row] == '' else df['Address'][row]
                company_name = None if df['Owner'][row] == '' else df['Owner'][row]
                phone_number = None if df['Contact'][row] == '' else df['Contact'][row]
                email = None if df['Email'][row] == '' else df['Email'][row]
                certification_number = 0 if df['Certificate No'][row] == '' else df['Certificate No'][row]
                renewal_date = 0 if df['Renewal Date'][row] == '' else df['Renewal Date'][row]
                validity = 0 if df['Validity'][row] == '' else df['Validity'][row]
                remarks = None if df['Remarks'][row] == '' else df['Remarks'][row]
                initial_issued_date = 0 if df['Initial Issued Date'][row] == '' else df['Initial Issued Date'][row]
                color = None if df['Color'][row] == '' else df['Color'][row]
                unid = None if df['UIN'][row] == '' else df['UIN'][row]
                popular_name = None if df['UAV Manufacturer & Model'][row] == '' else df['UAV Manufacturer & Model'][
                    row]
                registration_mark = None if df['Serial No.'][row] == '' else df['Serial No.'][row]
                begin_date = 0 if df['Date of Manufacture'][row] == '' else df['Date of Manufacture'][row]
                category = None if df['Drone Type'][row] == '' else df['Drone Type'][row]
                mass = None if df['Weight ( in Kg)'][row] == '' else df['Weight ( in Kg)'][row]
                addressdata = Address.objects.update_or_create(
                    address_line_1=address,
                )
                manufacturerdata, created_manufacturer = Manufacturer.objects.update_or_create(
                    address=Address.objects.get(address_line_1=address),
                    full_name=manufacturer
                )
                operator, created_operator = Operator.objects.update_or_create(
                    address=Address.objects.get(address_line_1=address),
                    company_name=company_name,
                    phone_number=phone_number,
                    email=email,
                )
                aircraft = Aircraft.objects.update_or_create(
                    manufacturer=Manufacturer.objects.get(id=manufacturerdata.id),
                    operator=Operator.objects.get(id=operator.id),
                    certification_number=certification_number,
                    renewal_date=renewal_date,
                    validity=validity,
                    remarks=remarks,
                    initial_issued_date=initial_issued_date,
                    color=color,
                    unid=unid,
                    popular_name=popular_name,
                    category=category,
                    mass=mass,
                    registration_mark=registration_mark,
                    begin_date=begin_date

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
            except KeyError as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + "Field is wrong")
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Sheet Uploaded ")
        return redirect('/np/dashboard/operators', messages)


class AboutPageView(TemplateView):
    template_name = 'flightres/about.html'


class GuidelinesPageView(TemplateView):
    template_name = 'flightres/guidelines.html'


class OperdatorDatabaseView(LoginRequiredMixin, ListView):
    template_name = 'flightres/operators_db.html'
    queryset = Aircraft.objects.all().order_by('-unid')

    def get_context_data(self, **kwargs):
        data = super(OperdatorDatabaseView, self).get_context_data(**kwargs)
        countdata = int(1)
        mandata = Manufacturer.objects.order_by('full_name')
        opedata = Operator.objects.order_by('company_name')
        data['test'] = FlightPermission.objects.order_by('uav_uuid')
        data['countdata'] = countdata
        data['mandata'] = mandata
        data['opedata'] = opedata

        return data


def dronedataupload(request):
    if request.method == 'POST':
        addressdata = Address.objects.update_or_create(
            address_line_1=request.POST['address']
        )
        manufacturerdata = Manufacturer.objects.create(
            address=Address.objects.get(address_line_1=request.POST['address']),
            full_name=request.POST['full_name']
        )
        operator = Operator.objects.create(
            address=Address.objects.get(address_line_1=request.POST['address']),
            company_name=request.POST['company_name'],
            phone_number=request.POST['phone_number'],
            email=request.POST['email'],
        )
        aircraft = Aircraft.objects.update_or_create(
            manufacturer=Manufacturer.objects.get(id=manufacturerdata.id),
            operator=Operator.objects.get(id=operator.id),
            certification_number=request.POST['certification_number'],
            renewal_date=request.POST['renewal_date'],
            validity=request.POST['validity'],
            remarks=request.POST['remarks'],
            initial_issued_date=request.POST['initial_issued_date'],
            color=request.POST['color'],
            unid=request.POST['unid'],
            category=request.POST['category'],
            mass=request.POST['mass'],
            registration_mark=request.POST['registration_mark'],
            begin_date=request.POST['begin_date']

        )
        mandata = Manufacturer.objects.order_by('full_name')
        opedata = Operator.objects.order_by('company_name')
        queryset = Aircraft.objects.all().order_by('-unid')
        test = FlightPermission.objects.order_by('uav_uuid')
        context = {
            'metadata': mandata,
            'opedata': opedata,
            'object_list': queryset,
            'test': test

        }
        messages.add_message(request, messages.SUCCESS, " Drone Profile Created ")
        return render(request, 'flightres/operators_db.html', context)
    else:
        mandata = Manufacturer.objects.order_by('full_name')
        opedata = Operator.objects.order_by('company_name')
        queryset = Aircraft.objects.all().order_by('-unid')
        test = FlightPermission.objects.order_by('uav_uuid')
        context = {
            'metadata': mandata,
            'opedata': opedata,
            'object_list': queryset,
            'test': test

        }
        return render(request, 'flightres/operators_db.html', context)


def dronedataupdate(request, pk):
    if request.method == 'POST':
        test1 = Aircraft.objects.get(id=pk)
        foraircraft = Aircraft.objects.filter(id=pk)
        test2 = Manufacturer.objects.get(id=test1.manufacturer.id)
        test4 = Operator.objects.get(id=test1.operator.id)

        test3 = Address.objects.get(id=test2.address.id)
        test3.address_line_1 = request.POST['address']
        test3.save()
        test2.full_name = request.POST['full_name']
        manufacturerdata = test2.save()
        test4.company_name = request.POST['company_name']
        test4.phone_number = request.POST['phone_number']
        test4.email = request.POST['email']
        operator = test4.save()
        aircraft = foraircraft.update(
            manufacturer=Manufacturer.objects.get(id=test2.id),
            operator=Operator.objects.get(id=test4.id),
            certification_number=request.POST['certification_number'],
            renewal_date=request.POST['renewal_date'],
            validity=request.POST['validity'],
            remarks=request.POST['remarks'],
            initial_issued_date=request.POST['initial_issued_date'],
            color=request.POST['color'],
            unid=request.POST['unid'],
            category=request.POST['category'],
            mass=request.POST['mass'],
            registration_mark=request.POST['registration_mark'],
            begin_date=request.POST['begin_date']

        )
        mandata = Manufacturer.objects.order_by('full_name')
        opedata = Operator.objects.order_by('company_name')
        queryset = Aircraft.objects.all().order_by('-unid')
        test = FlightPermission.objects.order_by('uav_uuid')
        context = {
            'metadata': mandata,
            'opedata': opedata,
            'object_list': queryset,
            'test': test

        }
        messages.add_message(request, messages.SUCCESS, " Drone Profile Updated ")
        return render(request, 'flightres/operators_db.html', context)
    else:
        mandata = Manufacturer.objects.order_by('full_name')
        opedata = Operator.objects.order_by('company_name')
        queryset = Aircraft.objects.all().order_by('-unid')
        test = FlightPermission.objects.order_by('uav_uuid')
        context = {
            'metadata': mandata,
            'opedata': opedata,
            'object_list': queryset,
            'test': test

        }
        return render(request, 'flightres/operators_db.html', context)


class OperatorAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Operator
    template_name = 'flightres/operators_db.html'
    form_class = OperatorForm
    success_url = '/np/dashboard/operators'
    success_message = ' Owner Added'


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
