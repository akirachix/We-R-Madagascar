from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
import base64
from flightres.models import Report, FlightPermission, Pilots, NoFlyZone
from flightres.utils import validate_lat_lon, is_near_senstive_area
from registry.models import Aircraft
from registry.models import SheetRegister
from registry.utils.preprocessor import Preprocessor
from .serializers import FlightRegistrySerializer, WhatsappComplainSerializer, \
    SheetRegisterSerializer, PilotsSerializer, PilotFromFlightSerializer, WhatsappComplainCreateSerializer
from zipfile import ZipFile
from datetime import date

@csrf_exempt
@xframe_options_exempt
def date_validation_view(request):
    if request.method == 'POST':
        try:
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            date_today = date.today()
            is_valid_start_date = (start_date_obj - date_today).days >= 0
            is_valid_date = (end_date_obj - start_date_obj).days >= 0
            if is_valid_start_date and is_valid_date:
                data = {
                    'valid': is_valid_date
                }
            else:
                data = {
                    'valid': False
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
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, **kwargs):
        print(request.data)
        serializer = FlightRegistrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg1 = str(serializer.data['uav_uid'])
            msg2 = str(serializer.data['status'])
            msg1_enc = msg1.encode('ASCII')
            msg1_crypt = base64.b64encode(msg1_enc)
            msg1_crypt_str = msg1_crypt.decode('ASCII')
            msg2_enc = msg2.encode('ASCII')
            msg2_crypt = base64.b64encode(msg2_enc)
            msg2_crypt_str = msg2_crypt.decode('ASCII')
            fin_msg = msg1_crypt_str + '$' + msg2_crypt_str
            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
            response_data = uri + str(serializer.data['uav_uid'])
            data = {
                'url': 'https://droneregistry.naxa.com.np/np/dashboard/request_response/' + fin_msg,
                'id' : str(serializer.data['uav_uid'])
                }
            return JsonResponse(data, status=status.HTTP_200_OK)

        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WhComplainView(ModelViewSet):
    queryset = Report.objects.all()

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

    def get_serializer_class(self):
        if self.action == 'create':
            return WhatsappComplainCreateSerializer
        else:
            return WhatsappComplainSerializer

    def create(self, request, **kwargs):
        serializer = WhatsappComplainCreateSerializer(data=request.data)
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
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
            # response_data = uri + str(serializer.data['uav_uid'])

            sheet = serializer.data.get('upload_sheet')
            print(sheet)
            # name = serializer.data.get('name')
            # user = serializer.data.get('created_by')

            excel_processor = Preprocessor(
                sheet, "x", "y")
            data_response = excel_processor.parse()
            if data_response[0] == 200:
                response = Response(status=data_response[0], data={'data': serializer.data,
                                                                   'message': data_response[1]})
                return response
            else:
                response = Response(status=data_response[0], data={'data': serializer.data,
                                                                   'message': data_response[1]})
                return response
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST, data={'data': serializer.errors,
                                                                          'message': 'Bad Request'})
            return response


class GeoLocationValidation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        message = "The provided latitude longitude is invalid format"
        lat_lon = data.get('lat_lon')
        is_valid_lat_lon = False
        is_near_sensitive_area = False
        print(lat_lon)

        is_valid_lat_lon, lat, lon = validate_lat_lon(lat_lon)

        if is_valid_lat_lon:
            no_fly_zone = NoFlyZone.objects.all()
            shp_names = []
            if no_fly_zone != None:
                count = -1
                for x in no_fly_zone:
                    count += 1
                    if str(x.spatialdata_zip_file).endswith('.zip'):
                        zipped = ZipFile(x.spatialdata_zip_file, 'r')
                        for y in zipped.namelist():
                            if y.endswith('.shp'):
                                shp_names.append(y.replace('.shp', '.geojson'))
                is_near_sensitive_area, message = is_near_senstive_area(lat, lon, shp_names)
            else:
                
                is_near_sensitive_area, message = is_near_senstive_area(lat, lon, shp_names)

        return JsonResponse(
            {'is_valid_lat_lon': is_valid_lat_lon,
             'is_not_near_sensitive_area': is_near_sensitive_area,
             'lat': lat,
             'lon': lon,
             'message': message,
             },
            status=status.HTTP_200_OK, )


class OldPermissionIdValidation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        try:
            permission_id = data.get('id')
            qs = FlightPermission.objects.filter(pk=permission_id)
            print(qs)
            print(permission_id)
    
            if qs.exists():
                pilot_id = FlightPermission.objects.get(
                    pk=permission_id).pilot_id.pk
                return JsonResponse(
                    {'valid': True, 'pilot_id': pilot_id}, status=status.HTTP_200_OK, )
            else:
                return JsonResponse(
                    {'valid': False,'error':'Id not found'},
                    status=status.HTTP_200_OK, )
        except ValueError:
            return JsonResponse(
                {'valid': False,'error':'exception'},
                status=status.HTTP_200_OK, )


class UniqueTeatDataView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        uin = data.get('uuid')
        try:
            if Aircraft.objects.filter(unid=uin).exists():
                return JsonResponse(
                    {'valid': True}, status=status.HTTP_200_OK, )
            else:
                return JsonResponse(
                    {'valid': False},
                    status=status.HTTP_200_OK, )
        except ValueError:
            return JsonResponse(
                {'valid': False},
                status=status.HTTP_200_OK, )


class PilotDetailAPIView(ModelViewSet):
    permission_classes = [AllowAny]
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
                data={'Message': "Pilot with ID {} not found. Please add pilot information".format(
                    kwargs['pk'])},
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
    permission_classes = [AllowAny]
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
                data={'Message': "Pilot with ID {} not found. Please add pilot information".format(
                    kwargs['pk'])},
                status=status.HTTP_400_BAD_REQUEST)
