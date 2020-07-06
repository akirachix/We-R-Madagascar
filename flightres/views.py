from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FlightPermission

class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission

@login_required
def approvePerm(request,pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'approve':
        selected_perm.is_approved = True
    elif action == 'deny':
        selected_perm.is_approved = False
    selected_perm.save()
    return redirect('/np/dashboard')

@login_required
def verifiedFlightresView(request, pk):
    selected_flight = get_object_or_404(FlightPermission, uav_uid=pk)
    return render(request, 'flightres/verified_pg.html', {'object': selected_flight})
