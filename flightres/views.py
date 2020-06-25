from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FlightPermission


class FlightPermissionList(LoginRequiredMixin, ListView):
    # specify the model for list view
    model = FlightPermission

def flightPermissionDetail(request, pk):
    perm = FlightPermission.objects.get(uav_uid = pk)
    return render(request, 'flightres/flightpermission_detail.html', {'perm': perm})

@login_required
def approvePerm(request,pk, action):
    selected_perm = get_object_or_404(FlightPermission, uav_uid=pk)
    if action == 'approve':
        selected_perm.is_approved = True
    elif action == 'deny':
        selected_perm.is_approved = False
    selected_perm.save()
    return redirect('/np/dashboard/flightperm_detail/{}'.format(pk))

