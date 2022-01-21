from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
# Create your views here.
from rest_framework import generics
# from .models import ClinicProfile
from django.views.generic import TemplateView,FormView ,CreateView
# from .forms import RegisterclinicForm
from django.core.paginator import InvalidPage,Paginator
from django.db.models import Q

# Create your views here.
# class ClinicCreateView(CreateView):
#     model=ClinicProfile
#     form_class=RegisterclinicForm
#     template_name='register_clinic.html'
#     success_url=reverse_lazy('view_clinic')
    

#     def form_valid(self,form):
#         return super (ClinicCreateView,self).form_valid(form)

# class ClinicViewDetails(ListView):
#     model=ClinicProfile
#     template_name='view_clinics.html'
#     context_object_name="clinics"

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
        
#         search_post = self.request.GET.get('search')
#         if search_post:
#             context['clinics']=context['clinics'].filter(Q(location__icontains=search_post)  | Q(clinic_name__icontains=search_post) )
#             context['results']=context['clinics'].count()
#         context['search_post']=search_post
#         return context

        
    


#     # def get(self, request, *args,**kwargs):
#     #     clinics=ClinicProfile.objects.all()
#     #     paginator=Paginator(clinics,30)
#     #     is_paginated=True if paginator.num_pages > 1 else False
#     #     page=request.GET.get("page") or 1
#     #     search_post = request.GET.get('search')
#     #     try:
#     #         current_page=paginator.page(page)
#     #     except InvalidPage as e:
#     #         raise Http404(str(e))

#     #     context={"clinics":current_page,"is_paginated":is_paginated}
#     #     return render(request,self.template_name,context)


    
# class ClinicUpdateView(UpdateView):
#     template_name='edit_clinic.html'
#     model=ClinicProfile
#     form_class=RegisterclinicForm
#     success_url=reverse_lazy("view_clinic")
    

#     def update_clinic(self,request,id):
#         clinic=ClinicProfile.objects.get(id=id)
#         form=RegisterclinicForm(request.POST,instance=clinic)
#         if form.is_valid():
#             form.save()
#         return render(request,self.template_name,{'form':form})


# # def search_clinic(request):
# #     search_post = request.GET.get('search')
# #     if search_post:
# #         clinics = ClinicProfile.objects.filter(Q(location__icontains=search_post))
# #         all_clinics = ClinicProfile.objects.all()
# #         results=clinics.count()
# #         return render (request,'view_clinics.html',{'clinics':clinics,'results':results,'all_clinics':all_clinics})
    
# #     return render (request,'view_clinics.html',{'clinics':clinics,'message':message}) 
        

    

