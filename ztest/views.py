from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import SessionWizardView
from ztest.forms import RequestForm

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from models import Request, Sequence, Album, Plan


class RequestWizard(SessionWizardView):
    
    SequenceFormSet = inlineformset_factory(Request, Sequence, extra=1)
    AlbumFormSet = inlineformset_factory(Sequence, Album, extra=1)
    PlanFormSet = inlineformset_factory(Album, Plan, extra=1)
    
    form_list = [RequestForm, SequenceFormSet, AlbumFormSet, PlanFormSet]
    template_name = 'ztest/wizard.html'
    
    def done(self, form_list, **kwargs):
        
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        
        for form in form_list:
            form.save()
        
        
        
#         if (form.is_valid() and Sequence_form.is_valid() and
#             Album_form.is_valid()) and Plan_form.is_valid():
#             return self.form_valid(form, Sequence_form, Album_form, Plan_form)
#         else:
#             return self.form_invalid(form, Sequence_form, Album_form, Plan_form)
#                                
            
        
   
    def form_valid(self, form, Sequence_form, Album_form, Plan_form):
        """
        Called if all forms are valid. Creates a Request instance along with
        associated Sequences and Albums and then redirects to a
        success page.
        """
        self.object = form.save()
        Sequence_form.instance = self.object
        Sequence_form.save()
        Album_form.instance = self.object
        Album_form.save()
        Plan_form.instance = self.object
        Plan_form.save()
        return render_to_response('ztest/result.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    
    def form_invalid(self, form, Sequence_form, Album_form, Plan_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  Sequence_form=Sequence_form,
                                  Album_form=Album_form,
                                  Plan_form=Plan_form))