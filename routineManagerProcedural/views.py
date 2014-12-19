from django.core import serializers
import os
import json
import time
from django.utils.encoding import smart_str
import mimetypes
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Request, Sequence, Album, Plan, SummaryManager
from forms import RequestForm, SequenceForm, AlbumForm, PlanForm
from common.models import OFTThreadManager
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    """redirect to index page """
         
    template = loader.get_template('routineManagerProcedural/index.html')
    email = request.user.email
    object_list = Request.objects.filter(email=email).order_by('-creation_date')
    context = RequestContext(request, {          
        'object_list': object_list, 
    })
 
    return HttpResponse(template.render(context))
    
@login_required
def request_create(request):
    """redirect to create page """
         
    template = loader.get_template('routineManagerProcedural/request_form.html')
    email = request.user.email
    laboratory = request.user.laboratory
    telnumber = request.user.telnumber    
    form = RequestForm(initial={'email': email, 'laboratory':laboratory, 'telnumber':telnumber, 'status':'INCOMPLETE'})
    context = RequestContext(request, {          
        'form': form, 
    })
 
    return HttpResponse(template.render(context))

@login_required
def request_save(request):
    """save request"""        
#     name = request.POST.get('name')
    email = request.POST.get('email')    
    choice = request.POST.get('action')
    instance = request.POST.get('instance')
    if(instance):
        req_in_db = Request.objects.get(id=instance) 
        form = RequestForm(instance=req_in_db, data=request.POST)     
    else:
        form = RequestForm(request.POST) 
    
#     form = RequestForm(request.POST)     
    
    if choice == 'export':
        
        queryset = Request.objects.filter(id=1)        
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        xml_serializer.serialize(queryset)
        """add a service which creates the xml instead of doing this"""
        with open("documents/request.xml", "w") as out:
            xml_serializer.serialize(queryset, stream=out)
               
        path = "documents/request.xml" # Get file path
        wrapper = FileWrapper( open( path, "r" ) )
        content_type = mimetypes.guess_type( path )[0]
    
        response = HttpResponse(wrapper, content_type = content_type)
        response['Content-Length'] = os.path.getsize( path ) # not FileField instance
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path ) ) # same here
       
        return response
    
    if choice == 'cancel':       
                
        template = loader.get_template('routineManagerProcedural/index.html')
        email = request.user.email
        object_list = Request.objects.filter(email=email).order_by('-creation_date')
        context = RequestContext(request, {          
            'object_list': object_list, 
        })
        
        
        return HttpResponse(template.render(context))
    
    
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
                global_summary = SummaryManager.get_summary(request_from_form.id);   
                template = loader.get_template('routineManagerProcedural/sequence_form.html')                   
                form = SequenceForm(initial={'status': 'INCOMPLETE'})
                form.request=request_from_form               
                context = RequestContext(request, {           
                    'form': form, 
                    'request_object':request_from_form,
                    'global_summary':global_summary
                })
                 
    else:
        global_summary = SummaryManager.get_summary(request_from_form.id);   
        template = loader.get_template('routineManagerProcedural/request_form.html')
        context = RequestContext(request, {          
            'form': form, 
            'global_summary':global_summary
        })
       
 
    return HttpResponse(template.render(context))

@login_required
def sequence_save(request):
    """save sequence"""
    
    
    choice = request.POST.get('action')
    form = SequenceForm(request.POST)    
    request_id = request.POST.get('request_id')
    request_object = Request.objects.get(id=request_id)   
    
    instance = request.POST.get('instance')
    if(instance):
        sequenceInDB = Sequence.objects.get(id=instance) 
        form = SequenceForm(instance=sequenceInDB, data=request.POST)     
    else:
        form = SequenceForm(request.POST) 
    
    if choice == 'cancel':
        global_summary = SummaryManager.get_summary(request_object.id);
        template = loader.get_template('routineManagerProcedural/request_form.html')        
        object_list = Sequence.objects.filter(request=request_object).order_by('-creation_date')
        form = RequestForm(instance=request_object)
        context = RequestContext(request, {          
            'object_list': object_list, 
            'form':form,
            'global_summary':global_summary
        })
        return HttpResponse(template.render(context))
    
    
    if(form.is_valid()): 
        """
        The following 4 lines are the way to save the object with its foreign key without adding
        a drop down list in the Form where the user selects the foreign key object    
        """       
        form.request = request_object
        sequence = form.save(commit=False) 
        sequence.request = request_object 
        sequence.save()               
        
        if choice == 'sequence_save_and_back':
            template = loader.get_template('routineManagerProcedural/request_form.html')
            """
                get the id of the request from the form, use it to get all sequences belonging to that request id, 
                and also send the form containing the request information
            """
            global_summary = SummaryManager.get_summary(request_object.id);
            object_list = Sequence.objects.filter(request=request_object).order_by('-creation_date')
            form = RequestForm(instance=request_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'global_summary':global_summary
            })
        else:
            if choice == 'sequence_save_and_add':
                template = loader.get_template('routineManagerProcedural/album_form.html') 
                global_summary = SummaryManager.get_summary(request_object.id);     
                form = AlbumForm(initial={'status': 'INCOMPLETE'})
                context = RequestContext(request, {          
                    'form': form, 
                    'sequence_object': sequence,
                    'global_summary':global_summary
                })
                 
    else:
        template = loader.get_template('routineManagerProcedural/sequence_form.html')
        global_summary = SummaryManager.get_summary(request_object.id);     
        context = RequestContext(request, {          
            'form': form, 
            'request_object':request_object,
            'global_summary':global_summary
        })
       
    print "no template so form is bad"
    return HttpResponse(template.render(context))

@login_required
def album_save(request):
    """save album"""
    
    
    choice = request.POST.get('action')
    form = AlbumForm(request.POST)    
    sequence_id = request.POST.get('sequence_id')
    sequence_object = Sequence.objects.get(id=sequence_id)   
    request_object = sequence_object.request
    
    instance = request.POST.get('instance')
    if(instance):
        albumInDB = Album.objects.get(id=instance) 
        form = AlbumForm(instance=albumInDB, data=request.POST)     
    else:
        form = AlbumForm(request.POST) 
    
    if choice == 'cancel':
        template = loader.get_template('routineManagerProcedural/sequence_form.html')
        global_summary = SummaryManager.get_summary(request_object.id);     
        object_list = Album.objects.filter(sequence=sequence_object).order_by('-creation_date')
        form = SequenceForm(instance=sequence_object)
        context = RequestContext(request, {          
            'object_list': object_list, 
            'form':form,
            'request_object':request_object,
            'global_summary':global_summary
        })
        return HttpResponse(template.render(context))
    
    
    if(form.is_valid()):        
        form.sequence = sequence_object
        album = form.save(commit=False) 
        album.sequence = sequence_object
        album.save()
        
        if choice == 'album_save_and_back':
            template = loader.get_template('routineManagerProcedural/sequence_form.html')
            global_summary = SummaryManager.get_summary(request_object.id);     
            object_list = Album.objects.filter(sequence=sequence_object).order_by('-creation_date')
            form = SequenceForm(instance=sequence_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'request_object':request_object,
                'global_summary':global_summary
            })
        else:
            if choice == 'album_save_and_add':
                template = loader.get_template('routineManagerProcedural/plan_form.html')  
                global_summary = SummaryManager.get_summary(request_object.id);         
                form = PlanForm(initial={'status': 'INCOMPLETE'})
                context = RequestContext(request, {          
                    'form': form, 
                    'album_object': album,
                    'global_summary':global_summary
                })
                 
    else:
        template = loader.get_template('routineManagerProcedural/album_form.html')
        global_summary = SummaryManager.get_summary(request_object.id);       
#         id_seq = sequence_object.id
        object_list = Plan.objects.filter
        context = RequestContext(request, {          
            'form': form, 
            'sequence_object':sequence_object,
            'global_summary':global_summary
        })
       
 
    return HttpResponse(template.render(context))

@login_required
def plan_save(request):
    """save plan"""
    
    choice = request.POST.get('action')
    form = PlanForm(request.POST)    
    album_id = request.POST.get('album_id')
    album_object = Album.objects.get(id=album_id)   
    sequence_object = album_object.sequence
    
    instance = request.POST.get('instance')
    if(instance):
        planInDB = Plan.objects.get(id=instance) 
        form = PlanForm(instance=planInDB, data=request.POST)     
    else:
        form = PlanForm(request.POST)       
    
    if choice == 'cancel':
            template = loader.get_template('routineManagerProcedural/album_form.html')
            global_summary = SummaryManager.get_summary(sequence_object.request.id);       
            object_list = Plan.objects.filter(album=album_object).order_by('-creation_date')
            form = AlbumForm(instance=album_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'sequence_object':sequence_object,
                'global_summary':global_summary
            })
            return HttpResponse(template.render(context))
            
    if(form.is_valid()):        
        form.album = album_object
        plan = form.save(commit=False) 
        plan.album = album_object
        plan.save()
        
        if choice == 'plan_save_and_back':
            template = loader.get_template('routineManagerProcedural/album_form.html')
            global_summary = SummaryManager.get_summary(sequence_object.request.id);   
            object_list = Plan.objects.filter(album=album_object).order_by('-creation_date')
            form = AlbumForm(instance=album_object)
            context = RequestContext(request, {          
                'object_list': object_list, 
                'form':form,
                'sequence_object':sequence_object,
                'global_summary':global_summary
            })
        
                 
    else:
        template = loader.get_template('routineManagerProcedural/plan_form.html')
        global_summary = SummaryManager.get_summary(sequence_object.request.id);   
        context = RequestContext(request, {          
            'form': form, 
            'album_object':album_object,
            'global_summary':global_summary
        })
       
 
    return HttpResponse(template.render(context))

@login_required
def edit_request(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    choice = request.GET.get('action')
    request_object = Request.objects.get(id=slug)
    if choice == 'edit':    
        template = loader.get_template('routineManagerProcedural/request_form.html')
        global_summary = SummaryManager.get_summary(slug);        
        form=RequestForm(instance=request_object)
        object_list = Sequence.objects.filter(request=request_object)
        context = RequestContext(request, {     
                'instance':request_object.id,                                
                'form': form, 
                'object_list':object_list,
                'global_summary':global_summary
            })
    else:
        if choice == 'delete':
            request_object.delete()
            template = loader.get_template('routineManagerProcedural/index.html')
            email = request.user.email
            object_list = Request.objects.filter(email=email).order_by('-creation_date')
            context = RequestContext(request, {          
                'object_list': object_list, 
            })

    return HttpResponse(template.render(context))

@login_required
def edit_sequence(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    choice = request.GET.get('action')
    sequence_object = Sequence.objects.get(id=slug)
    request_object = sequence_object.request
    if choice == 'edit':
        template = loader.get_template('routineManagerProcedural/sequence_form.html')  
        global_summary = SummaryManager.get_summary(request_object.id);         
        form=SequenceForm(instance=sequence_object)
        object_list = Album.objects.filter(sequence=sequence_object)
        context = RequestContext(request, {     
                'instance':sequence_object.id,     
                'form': form, 
                'object_list':object_list,
                'request_object':request_object,
                'global_summary':global_summary
            })
    else:
        if choice == 'delete':
            sequence_object.delete()
            template = loader.get_template('routineManagerProcedural/request_form.html')  
            global_summary = SummaryManager.get_summary(request_object.id); 
            form=RequestForm(instance=request_object)
            object_list = Sequence.objects.filter(request=request_object)
            context = RequestContext(request, {          
                    'form': form, 
                    'object_list':object_list,
                    'global_summary':global_summary
                })
            
    return HttpResponse(template.render(context))

@login_required
def edit_album(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    choice = request.GET.get('action')
    
    album_object = Album.objects.get(id=slug)
    sequence_object = album_object.sequence
    request_object = sequence_object.request
    if choice == 'edit':
        template = loader.get_template('routineManagerProcedural/album_form.html')
        global_summary = SummaryManager.get_summary(request_object.id);
        form=AlbumForm(instance=album_object)
        object_list = Plan.objects.filter(album=album_object)
        context = RequestContext(request, {
                'instance':album_object.id,          
                'form': form, 
                'object_list':object_list,
                'sequence_object':sequence_object,
                'global_summary':global_summary
            })
    else:
        if choice == 'delete':
            album_object.delete()
            template = loader.get_template('routineManagerProcedural/sequence_form.html')      
            global_summary = SummaryManager.get_summary(request_object.id);          
            form=SequenceForm(instance=sequence_object)
            object_list = Album.objects.filter(sequence=sequence_object)
            context = RequestContext(request, {          
                    'form': form, 
                    'object_list':object_list,
                    'request_object':request_object,
                    'global_summary':global_summary
                })

    return HttpResponse(template.render(context))

@login_required
def edit_plan(request, slug):
    
    """get slug, get list of objects and instantiate form"""
    choice = request.GET.get('action')    
    plan_object = Plan.objects.get(id=slug)
    album_object = plan_object.album
    sequence_object = album_object.sequence
    if choice == 'edit':
        template = loader.get_template('routineManagerProcedural/plan_form.html')
        global_summary = SummaryManager.get_summary(sequence_object.request.id);        
        form = PlanForm( instance = plan_object)            
        context = RequestContext(request, {  
                'instance':plan_object.id,          
                'form': form,             
                'album_object':album_object,
                'global_summary':global_summary
            })
    else:
        if choice == 'delete':
            plan_object.delete()
            template = loader.get_template('routineManagerProcedural/album_form.html')       
            global_summary = SummaryManager.get_summary(sequence_object.request.id);        
            form=AlbumForm(instance=album_object)
            object_list = Plan.objects.filter(album=album_object)
            context = RequestContext(request, {          
                    'form': form, 
                    'object_list':object_list,
                    'sequence_object':sequence_object,
                    'global_summary':global_summary
                })

    return HttpResponse(template.render(context))

@login_required
def help_request(request):
    template = loader.get_template('routineManagerProcedural/help_request.html')
    context = RequestContext(request, {          
                    
                })

    return HttpResponse(template.render(context))

@login_required
def help_sequence(request):
    template = loader.get_template('routineManagerProcedural/help_sequence.html')
    context = RequestContext(request, {          
                    
                })

    return HttpResponse(template.render(context))

@login_required
def help_album(request):
    template = loader.get_template('routineManagerProcedural/help_album.html')
    context = RequestContext(request, {          
                    
                })

    return HttpResponse(template.render(context))

@login_required
def help_plan(request):
    template = loader.get_template('routineManagerProcedural/help_plan.html')
    context = RequestContext(request, {          
                    
                })

    return HttpResponse(template.render(context))

@login_required
def getJd1Jd2(request):
#     time.sleep(20)
    location = request.GET.get('slug', '')    
    result = OFTThreadManager.getJd1Jd2(location)    
    if result == None or result == "":
        result = 'No data received' 
    data = ( {'jd1':result[0] , 'jd2':result[1] })
    convertedJSON = json.dumps(data, ensure_ascii=False)   
    
    return HttpResponse(convertedJSON)
    






