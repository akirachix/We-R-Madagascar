from django.shortcuts import render
from  flightres.models import WhatsappComplain, FlightRegistry
from  .serializers import  FlightRegistrySerializer, WhatsappComplainSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from  rest_framework import  status

class FlightRegistryView(ModelViewSet):
    queryset = FlightRegistry.objects.all()
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
        serializer = FlightRegistrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uri = "http://127.0.0.1:8000/np/api/v1/whcomplain/"
            response_data = uri + serializer.data['uav_uid']
            print(response_data, uri, serializer.data['uav_uid'])
            return Response({'track_url': response_data, 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class WhComplainView(ModelViewSet):
    queryset = WhatsappComplain.objects.all()
    serializer_class = WhatsappComplainSerializer

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
            response_data = uri + serializer.data['uav_uid']
            return Response({'track_url': response_data, 'data': serializer.data},status=status.HTTP_201_CREATED)
        return Response({'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST,)


       