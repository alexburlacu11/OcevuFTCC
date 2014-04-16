from django.views.generic import TemplateView
from django.views.generic import ListView
from alertManager.models import Alert
from routineManager.models import RoutineRequest
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render


class GenericView(TemplateView):
    template_name = "ztest/index.html"
    
    def post(self, request, *args, **kwargs):
        
        a = Alert(ivorn=request.POST['ivorn'] , author=request.POST['author'] , role=request.POST['role']  )
       
        a.save()
        return render(request, self.template_name, {'form': a})
    
      
    def create_object(self, request, *args, **kwargs):
        a = "Not implemented"
        return a
        
        

# class AlertIndexView(GenericView):
#     template_name = "alertmanager/index.html"
#     
#     @override
#     def create_object(self, request, *args, **kwargs):
#         a = Alert(ivorn=request.POST['ivorn'] , author=request.POST['author'] , role=request.POST['role']  )
#         
#         return a
#     
# class RequestIndexView(GenericView):
#     template_name = "routinemanager/index.html"
#     
#     @override
#     def create_object(self, request, *args, **kwargs):
#         a = RoutineRequest(name=request.POST['name'] , laboratory=request.POST['laboratory'] , telnumber=request.POST['telnumber']  )
# 
#         return a

class AlertListView(ListView):
    model = Alert
    paginate_by = 10
  

class AlertCreate(CreateView):
    model = Alert
    fields = ['ivorn','author','role']
    

class AlertUpdate(UpdateView):
    model = Alert
        

class AlertDelete(DeleteView):
    model = Alert
    success_url = reverse_lazy('alert-list')
    
class RoutineRequestListView(ListView):
    model = Alert
    paginate_by = 10
  

class RoutineRequestCreate(CreateView):
    model = Alert
    fields = ['ivorn','author','role']
    

class RoutineRequestUpdate(UpdateView):
    model = Alert
        

class RoutineRequestDelete(DeleteView):
    model = Alert
    success_url = reverse_lazy('alert-list')
    

    