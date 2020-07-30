from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.core import exceptions
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

from flightres.models import Report, FlightPermission, Pilots
from registry.models import Aircraft
from registry.models import SheetRegister
from registry.utils.preprocessor import Preprocessor
from .serializers import FlightRegistrySerializer, WhatsappComplainSerializer, \
    SheetRegisterSerializer, PilotsSerializer, PilotFromFlightSerializer


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
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, **kwargs):
        serializer = FlightRegistrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
            response_data = uri + str(serializer.data['uav_uid'])
            data = {'url': 'https://droneregistry.naxa.com.np/np/dashboard/request_response/' + str(
                serializer.data['uav_uid'])}
            return JsonResponse(data, status=status.HTTP_200_OK)

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

    def create(self, request, **kwargs):
        serializer = WhatsappComplainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/whcomplain/"
            response_data = uri + str(serializer.data['uav_uid'])
            return Response({'track_url': response_data, 'data': serializer.data}, status=status.HTTP_200_OK, )
        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST, )


class SheetUploadView(ModelViewSet):
    queryset = SheetRegister.objects.all()
    serializer_class = SheetRegisterSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SheetUploadView, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'list',
                           'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    def create(self, request):
        serializer = SheetRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
            # response_data = uri + str(serializer.data['uav_uid'])

            sheet = serializer.data.get('upload_sheet')

            excel_processor = Preprocessor(
                sheet,
                "x", "y")
            excel_processor.parse()

            return Response({
                'data': serializer.data},
                status=status.HTTP_200_OK, )
        return Response({'Message': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST, )


class UniqueTeatDataView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print(data)
        uin = data.get('uuid')
        print(uin)
        if Aircraft.objects.filter(unid=uin).exists():
            return Response(
                {'valid': True}, status=status.HTTP_200_OK, )
        else:
            return Response(
                {'valid': False},
                status=status.HTTP_200_OK, )


class PilotDetailAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pilots.objects.all()
    serializer_class = PilotsSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'list',
                           'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            return Response(serializer.data, status=200)
        except:
            return Response(
                data={'Message': "Pilot with ID {} not found. Please add pilot information".format(kwargs['pk'])},
                status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = PilotsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            base_uri = "http://127.0.0.1:8000/np/api/v1/pilot-data/"
            response_data = base_uri + str(serializer.data['id'])
            new_pilot_id = serializer.data['id']
            data = {'pilot_id': serializer.data['id']}
            return JsonResponse(data, status=status.HTTP_200_OK)

        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetPilotFromPermissionView(RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FlightPermission.objects.all()
    serializer_class = PilotFromFlightSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            return Response(serializer.data, status=200)
        except:
            return Response(
                data={'Message': "Pilot with ID {} not found. Please add pilot information".format(kwargs['pk'])},
                status=status.HTTP_400_BAD_REQUEST)
