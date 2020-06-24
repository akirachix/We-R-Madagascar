from django.shortcuts import render

from django.views.generic.list import ListView
from .models import FlightPermission


class FlightPermissionList(ListView):
    # specify the model for list view
    model = FlightPermission
