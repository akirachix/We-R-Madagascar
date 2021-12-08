from django.shortcuts import render
# Create your views here.
from rest_framework import generics, permissions
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
class ObtainTokenPairWithUserDetail(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
class CustomUserCreate(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class=UserSerializer
    def post(self, request, format='json'):
        serializer_context = {
            'request': request,
        }
        serializer = UserSerializer(data=request.data, context= serializer_context)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)