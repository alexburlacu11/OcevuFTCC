from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import SessionWizardView
from ztest.forms import RequestForm, SequenceForm, AlbumForm, PlanForm
from django.http import HttpResponseRedirect, HttpResponse

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from models import Request, Sequence, Album, Plan
from django.views.generic import ListView, CreateView

from django.views.generic import View

from django.template import Context


#     
# class RequestCreate(CreateView):
# #     template_name = 'Request_add.html'
#     model = Request
#     form_class = RequestForm
#     success_url = '/routinemanager2/new_sequence'
#     
#     def get_context_data(self, **kwargs):
#         context = super(RequestCreate, self).get_context_data(**kwargs)
#         context['seq_list'] = Sequence.objects.all()
#         return context   
# 
# class SequenceCreate(CreateView):
#     model = Sequence
#     form_class = SequenceForm
#     success_url = '/routinemanager2/new_album'
#     
#     def get_context_data(self, **kwargs):
#         context = super(SequenceCreate, self).get_context_data(**kwargs)
#         context['album_list'] = Album.objects.all()
#         return context
#     
#    
#         
# class AlbumCreate(CreateView):
#     model = Album
#     form_class = AlbumForm
#     success_url = '/routinemanager2/new_plan'
#     
#     def get_context_data(self, **kwargs):
#         context = super(AlbumCreate, self).get_context_data(**kwargs)
#         context['plan_list'] = Plan.objects.all()
#         return context
#     
#     
#         
# class PlanCreate(CreateView):
#     model = Plan
#     form_class = PlanForm
#     success_url = '/routinemanager2/'
           
    
    
class RequestIndex(ListView):
    
    model = Request
    template_name="ztest/index.html"
    context_object_name = 'request_list'
    
    def get_queryset(self):
        email = self.request.user.email
        return Request.objects.filter(email=email).order_by('-creation_date')    
    


class RequestWizard(SessionWizardView):
    
    form_list = [RequestForm, SequenceForm, AlbumForm, PlanForm]
    template_name = 'ztest/wizard.html'
         
    def get_context_data(self, form, **kwargs):
        context = super(RequestWizard, self).get_context_data(form=form, **kwargs)
        email = self.request.user.email
# #         request_id = context['request_id']
#         request = Request.objects.filter(email=email)
#         sequence_id = context['sequence_id']
#         album_id = context['album_id']
        
        r = Request.objects.filter(pk=1)
        
        if self.steps.current == '0':
            context.updateSequenceForConditions({'object_list': Sequence.objects.filter(request=r)})
        if self.steps.current == '1':
            
            email = self.request.user.email
           
            req = Request.objects.filter(email=email).order_by('-creation_date').first()
   
            context.updateSequenceForConditions({'object_list': Album.objects.all(), 'request':req})
            
        if self.steps.current == '2':
            context.updateSequenceForConditions({'object_list': Plan.objects.all()})
         
        return context
    
    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})  
        if self.steps.current == '0':      
            email = self.request.user.email        
            laboratory = self.request.user.laboratory
            telnumber = self.request.user.telnumber        
            initial.updateSequenceForConditions({                    
                        'email': email, 
                        'laboratory': laboratory, 
                        'telnumber': telnumber, 
                           })
        
            
            
        return initial
 
    def done(self, form_list, **kwargs):
         
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
         
        self.instance_dict = {}
        self.storage.reset()
            
        return HttpResponseRedirect('/routinemanager2/')
        
    
    def process_step(self, form):        
        
        if (form.is_valid()):
            if self.steps.current == '0':
                request = form.save()      
                id = request.id
#                 context.updateSequenceForConditions({'request_id': id})  
            if self.steps.current == '1':
                sequence = form.save()      
                id = sequence.id
#                 context.updateSequenceForConditions({'sequence_id': id})
            if self.steps.current == '2':
                album = form.save()      
                id = album.id
#                 context.updateSequenceForConditions({'album_id': id}) 
         
        return self.get_form_step_data(form)       
#             
            
#         
#         
#         
# #         if (form.is_valid() and Sequence_form.is_valid() and
# #             Album_form.is_valid()) and Plan_form.is_valid():
# #             return self.form_valid(form, Sequence_form, Album_form, Plan_form)
# #         else:
# #             return self.form_invalid(form, Sequence_form, Album_form, Plan_form)
# #                                
#             
#         
#    
#     def form_valid(self, form, Sequence_form, Album_form, Plan_form):
#         """
#         Called if all forms are valid. Creates a Request instance along with
#         associated Sequences and Albums and then redirects to a
#         success page.
#         """
#         self.object = form.save()
#         Sequence_form.instance = self.object
#         Sequence_form.save()
#         Album_form.instance = self.object
#         Album_form.save()
#         Plan_form.instance = self.object
#         Plan_form.save()
#         return render_to_response('ztest/result.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })
#     
#     def form_invalid(self, form, Sequence_form, Album_form, Plan_form):
#         """
#         Called if a form is invalid. Re-renders the context data with the
#         data-filled forms and errors.
#         """
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   Sequence_form=Sequence_form,
#                                   Album_form=Album_form,
#                                   Plan_form=Plan_form))