from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Request, Sequence, Album, Plan
from forms import RequestForm, SequenceForm, AlbumForm, PlanForm
# Create your views here.


def index(request):
    """redirect to index page """
         
    template = loader.get_template('routineManagerProcedural/index.html')
    email = request.user.email
    object_list = Request.objects.filter(email=email).order_by('-creation_date')
    context = RequestContext(request, {          
        'object_list': object_list, 
    })
 
    return HttpResponse(template.render(context))
    
def request_create(request):
    """redirect to create page """
         
    template = loader.get_template('routineManagerProcedural/request_form.html')
    email = request.user.email
    laboratory = request.user.laboratory
    telnumber = request.user.telnumber    
    form = RequestForm(initial={'email': email, 'laboratory':laboratory, 'telnumber':telnumber})
    context = RequestContext(request, {          
        'form': form, 
    })
 
    return HttpResponse(template.render(context))

def request_save(request):
    """save request"""
    
    name = request.POST.get('name')
    email = request.POST.get('email')    
    choice = request.POST.get('action')
#     instance = Request.objects.get(name=name, email=email)
#     if(instance):
#         form = RequestForm(instance=instance)     
#     else:
#         form = RequestForm(request.POST or None) 
    
    form = RequestForm(request.POST)     
    if(form.is_valid()):
        """check if it exists"""
#         request_db = get_object_or_404(Request, name=name, email=email)
        request_from_form = form.save()
        if choice == 'request_save_and_back':
            template = loader.get_template('routineManagerProcedural/index.html')
            email = request.user.email
            object_list = Request.objects.filter(email=email).order_by('-creation_date')
            context = RequestContext(request, {          
                'object_list': object_list, 
            })
        else:
            if choice == 'request_save_and_add':
                template = loader.get_template('routineManagerProcedural/sequence_form.html')                   
                form = SequenceForm()
                form.request=request_from_form
                context = RequestContext(request, {           
                    'form': form, 
                    'request_object':request_from_form
                })
                 
    else:
        template = loader.get_template('routineManagerProcedural/request_form.html')
        context = RequestContext(request, {          
            'form': form, 
        })
       
 
    return HttpResponse(template.render(context))

def sequence_save(request):
    """save sequence"""
    
    choice = request.POST.get('action')
    form = SequenceForm(request.POST)    
    request_id = request.POST.get('request_id')
    request_object = Request.objects.get(id=request_id)   
    if(form.is_valid()):        
        form.request = request_object
        sequence = form.save() 
        
        if choice == 'sequence_save_and_back':
            template = loader.get_template('routineManagerProcedural/request_form.html')
            """
                get the id of the request from the form, use it to get all sequences belonging to that request id, 
                and also send the form containing the request information
            """
            
            object_list = Sequence.objects.filter(request=request_object).order_by('-creation_date')
            form = RequestForm(instance=request_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form
            })
        else:
            if choice == 'sequence_save_and_add':
                template = loader.get_template('routineManagerProcedural/album_form.html')      
                form = AlbumForm()
                context = RequestContext(request, {          
                    'form': form, 
                    'sequence_object': sequence
                })
                 
    else:
        template = loader.get_template('routineManagerProcedural/sequence_form.html')
        context = RequestContext(request, {          
            'form': form, 
            'request_object':request_object
        })
       
 
    return HttpResponse(template.render(context))


def album_save(request):
    """save album"""
    
    choice = request.POST.get('action')
    form = AlbumForm(request.POST)    
    sequence_id = request.POST.get('sequence_id')
    sequence_object = Sequence.objects.get(id=sequence_id)   
    request_object = sequence_object.request
    
    if(form.is_valid()):        
        form.sequence = sequence_object
        album = form.save() 
        
        if choice == 'album_save_and_back':
            template = loader.get_template('routineManagerProcedural/sequence_form.html')
            object_list = Album.objects.filter(sequence=sequence_object).order_by('-creation_date')
            form = SequenceForm(instance=sequence_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'request_object':request_object,
            })
        else:
            if choice == 'album_save_and_add':
                template = loader.get_template('routineManagerProcedural/plan_form.html')      
                form = PlanForm()
                context = RequestContext(request, {          
                    'form': form, 
                    'album_object': album
                })
                 
    else:
        template = loader.get_template('routineManagerProcedural/album_form.html')
        id_seq = sequence_object.id
        object_list = Plan.objects.filter
        context = RequestContext(request, {          
            'form': form, 
            'sequence_object':sequence_object,
            
        })
       
 
    return HttpResponse(template.render(context))


def plan_save(request):
    """save plan"""
    
    choice = request.POST.get('action')
    form = PlanForm(request.POST)    
    album_id = request.POST.get('album_id')
    album_object = Album.objects.get(id=album_id)   
    sequence_object = album_object.sequence
    if(form.is_valid()):        
        form.album = album_object
        plan = form.save() 
        
        if choice == 'plan_save_and_back':
            template = loader.get_template('routineManagerProcedural/album_form.html')
            object_list = Plan.objects.filter(album=album_object).order_by('-creation_date')
            form = AlbumForm(instance=album_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'sequence_object':sequence_object,
            })
        
                 
    else:
        template = loader.get_template('routineManagerProcedural/plan_form.html')
        context = RequestContext(request, {          
            'form': form, 
            'album_object':album_object
        })
       
 
    return HttpResponse(template.render(context))


def edit_request(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    
    template = loader.get_template('routineManagerProcedural/request_form.html')
    request_object = Request.objects.get(id=slug)
    form=RequestForm(instance=request_object)
    object_list = Sequence.objects.filter(request=request_object)
    context = RequestContext(request, {          
            'form': form, 
            'object_list':object_list
        })

    return HttpResponse(template.render(context))

def edit_sequence(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    
    template = loader.get_template('routineManagerProcedural/sequence_form.html')
    sequence_object = Sequence.objects.get(id=slug)
    request_object = sequence_object.request
    form=SequenceForm(instance=sequence_object)
    object_list = Album.objects.filter(sequence=sequence_object)
    context = RequestContext(request, {          
            'form': form, 
            'object_list':object_list,
            'request_object':request_object
        })

    return HttpResponse(template.render(context))

def edit_album(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    
    template = loader.get_template('routineManagerProcedural/album_form.html')
    album_object = Album.objects.get(id=slug)
    sequence_object = album_object.sequence
    form=AlbumForm(instance=album_object)
    object_list = Plan.objects.filter(album=album_object)
    context = RequestContext(request, {          
            'form': form, 
            'object_list':object_list,
            'sequence_object':sequence_object
        })

    return HttpResponse(template.render(context))

def edit_plan(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    
    template = loader.get_template('routineManagerProcedural/plan_form.html')
    plan_object = Plan.objects.get(id=slug)
    album_object = plan_object.album
    form=PlanForm(instance=plan_object)    
    context = RequestContext(request, {          
            'form': form,             
            'album_object':album_object
        })

    return HttpResponse(template.render(context))


