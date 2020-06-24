from django.shortcuts import render

from django.views.generic.list import ListView
from .models import FlightPermission


class GeeksList(ListView):
    # specify the model for list view
    model = FlightPermission
