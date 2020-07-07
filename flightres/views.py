from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FlightPermission, Report

class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission

@login_required
def approvePerm(request,pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'approve':
        selected_perm.status = 'Approved'
    elif action == 'deny':
        selected_perm.status = 'Rejected'
    selected_perm.save()
    return redirect('/np/dashboard')

@login_required
def flightReqResponseView(request, pk):
    selected_flight = get_object_or_404(FlightPermission, uav_uid=pk)
    if selected_flight.status == 'Approved':
        return render(request, 'flightres/verified_pg.html', {'object': selected_flight})
    elif selected_flight.status == 'Rejected':
        return render(request, 'flightres/reject_pg.html', {'object': selected_flight})
    else:
        return render(request, 'flightres/pending_pg.html')

class ComplainListView(LoginRequiredMixin, ListView):
    template_name = 'flightres/complaint_management.html'
    model = Report