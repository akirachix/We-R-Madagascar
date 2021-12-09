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
from .models import ClinicProfile
from django.views.generic import TemplateView,FormView ,CreateView
from .forms import RegisterclinicForm
from django.core.paginator import InvalidPage,Paginator



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

class ClinicCreateView(CreateView):
    model=ClinicProfile
    form_class=RegisterclinicForm
    template_name='register_clinic.html'
    success_url=reverse_lazy('dashboard:dashboard')
    

    def form_valid(self,form):
        return super (ClinicCreateView,self).form_valid(form)

class ClinicViewDetails(ListView):
    model=ClinicProfile
    template_name='view_clinics.html'

    def get(self, request, *args,**kwargs):
        clinics=ClinicProfile.objects.all()
        paginator=Paginator(clinics,30)
        is_paginated=True if paginator.num_pages > 1 else False
        page=request.GET.get("page") or 1
        try:
            current_page=paginator.page(page)
        except InvalidPage as e:
            raise Http404(str(e))

        context={"clinics":current_page,"is_paginated":is_paginated}
        return render(request,self.template_name,context)

    
class ClinicUpdateView(UpdateView):
    template_name='edit_clinic.html'
    model=ClinicProfile
    form_class=RegisterclinicForm
    success_url=reverse_lazy("view_clinic")
    

    def update_clinic(self,request,id):
        clinic=ClinicProfile.objects.get(id=id)
        form=RegisterclinicForm(request.POST,instance=clinic)
        if form.is_valid():
            form.save()
        return render(request,self.template_name,{'form':form})
        







