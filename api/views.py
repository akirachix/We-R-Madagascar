from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from flightres.models import Report, FlightPermission
from registry.models import Aircraft
from registry.models import SheetRegister
from registry.utils.preprocessor import Preprocessor
from .serializers import FlightRegistrySerializer, WhatsappComplainSerializer, \
    SheetRegisterSerializer


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

    def create(self, request, **kwargs):
        serializer = FlightRegistrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            uri = "http://127.0.0.1:8000/np/api/v1/flightres/"
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
        uin = data.get('unid')
        print(uin)
        if Aircraft.objects.filter(unid=uin).exists():
            return Response(
                {'valid': True}, status=status.HTTP_200_OK, )
        else:
            return Response(
                {'data': False},
                status=status.HTTP_200_OK, )
