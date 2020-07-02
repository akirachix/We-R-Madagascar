from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from twilio.twiml.messaging_response import MessagingResponse

from flightres.models import Report, FlightPermission
from .serializers import FlightRegistrySerializer, WhatsappComplainSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse


@csrf_exempt
@xframe_options_exempt
def date_validation_view(request):
    if request.method == 'POST':
        try:
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            is_valid_date = (end_date_obj - start_date_obj).days > 0
            data = {
                'valid': is_valid_date
            }

            return JsonResponse(data)

        except MultiValueDictKeyError as e:
            return JsonResponse({})
    else:
        return HttpResponse("")


class FlightRegistryView(ModelViewSet):
    queryset = FlightPermission.objects.all()
    serializer_class = FlightRegistrySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        print(request.data)
        serializer = FlightRegistrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/whcomplain/"
            response_data = uri + str(serializer.data['uav_uid'])
            print(response_data, uri, serializer.data['uav_uid'])
            return Response({'track_url': response_data, 'data': serializer.data}, status=status.HTTP_200_OK,
                            content_type="application/json")
        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WhComplainView(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = WhatsappComplainSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WhComplainView, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = WhatsappComplainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
            response_data = uri + str(serializer.data['uav_uid'])
            return Response({'track_url': response_data, 'data': serializer.data}, status=status.HTTP_200_OK, )
        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, )
