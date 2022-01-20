from django.core import paginator
from django.db.models.base import Model
from django.http.response import Http404
from django.shortcuts import render
from django.views import generic
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
# Create your views here.
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework import generics
from django.views.generic import TemplateView,FormView ,CreateView
from django.core.paginator import InvalidPage,Paginator
from django.db.models import Q



class ObtainTokenPairWithUserDetail(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class CustomUserCreate(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

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











