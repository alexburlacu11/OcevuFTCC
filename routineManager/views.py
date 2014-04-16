from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

#QUE DE L AFFICHAGE formattage dans la vue, le model recupere des donnees, recuperation et enregistrement

from django.core.urlresolvers import reverse

from forms import DocumentForm
from models import Document
from models import RoutineRequest
from forms import RoutineRequestForm


def add(request):
    """redirect to add page """

    template = loader.get_template('routinemanager/add.html')   
    request_form = RoutineRequestForm() 
    context = RequestContext(request, { 
        'form':request_form,                                  
    })

    return HttpResponse(template.render(context))

def list(request):
    """redirect to list page """
      
    template = loader.get_template('routinemanager/list.html')
    ev = RoutineRequest()
    routine_requests = ev.getAll()    
    context = RequestContext(request, { 
        'requests': routine_requests,  
    })

    return HttpResponse(template.render(context))

def edit(request):
    """redirect to edit page """
    id = request.POST['id'] 
    
    template = loader.get_template('routinemanager/edit.html')
    ev = RoutineRequest()
    
    event = ev.get(id)
   
    form = RoutineRequestForm(instance=event)    
        
    context = RequestContext(request, {          
        'form' : form,
        'id' : id
    })


    return HttpResponse(template.render(context))

def delete(request):
    """ redirect to main page """
    id = request.POST['id'] 
    template = loader.get_template('routinemanager/index.html')
    ev2 = RoutineRequest()
    evv = ev2.get(id)
    evv.delete()
    ev = RoutineRequest()
    events = ev.getAll()    
    success = True
    context = RequestContext(request, {          
        'events': events,  
        'success' : success,
    })
    
    
    return HttpResponse(template.render(context))


def view(request):
#     get routine request and send it to page
    id = request.POST['id'] 
    template = loader.get_template('routinemanager/view.html')
    
    ev = RoutineRequest()
    a = ev.get(id)
    context = RequestContext(request, {          
        'a':a, 
        'id':id,
    })
    
    return HttpResponse(template.render(context))


    
def index(request):
    """main index page of routine manager"""
    template = loader.get_template('routinemanager/index.html') 
   
    context = RequestContext(request, {          
    
    })

    return HttpResponse(template.render(context))

def loadfromfile(request):
    """redirect to loadfromfile page """
        
    template = loader.get_template('routinemanager/loadfromfile.html')
    form = DocumentForm()
    context = RequestContext(request, {          
        'form': form, 
    })

    return HttpResponse(template.render(context))

def upload_file(request):
    """upload routine request to the server for analysis"""
    ev = RoutineRequest()
    myevents = ev.getAll()
        
    # Handle file upload
    try:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.save()    
                filename = request.FILES['docfile'].name
                template = loader.get_template('routinemanager/routinerequestviewer.html')    
                v = RoutineRequest()
                data = v.loadRequestFromXML("documents/"+filename)            
                context = RequestContext(request, {                  
                    'a': data,      
                })
            
                return HttpResponse(template.render(context))
            else:
                e = 1
                form = DocumentForm()
                return render_to_response('routinemanager/loadfromfile.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    except:   
        e = 2
        form = DocumentForm(request.POST, request.FILES)      
        return render_to_response('routinemanager/loadfromfile.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
def routine_request_to_db(request):
    """insert request in database"""
    
    try:
        if request.method == 'POST':
            form = RoutineRequestForm(request.POST)
            if form.is_valid():
                     
                """ scientific validation here """
                
                req = RoutineRequest(
                    name = request.POST['name'],
                    laboratory = request.POST['laboratory'],
                    telnumber = request.POST['telnumber'],
                    email = request.POST['email'],
                    creation_date = request.POST['creation_date'],
                    request_is_ALERT = (True if request.POST['request_is_ALERT']==True else False),
                    seq_number = int(request.POST['seq_number']),   
                )
                                                
                req.save()  
                  
                template = loader.get_template('routinemanager/index.html')                    
                success = True
                context = RequestContext(request, {                                        
                    'success' : success,       
                })
                
                return HttpResponse(template.render(context))
            else:
                e = 1
                print("invalid form")
                myform = RoutineRequestForm(request.POST)
                return render_to_response('routinemanager/add.html', {'form': myform, 'error': e, }, context_instance=RequestContext(request))
        
    except Exception, ex:  
        e = 2
        myform = RoutineRequestForm(request.POST)
        return render_to_response('routinemanager/add.html', {'form': myform, 'error': e, }, context_instance=RequestContext(request))
        
def update_to_db(request):
    """update routine request in database"""
    
    try:
        if request.method == 'POST':
            form = RoutineRequestForm(request.POST)
            id = request.POST['id']
            if form.is_valid():

                """ scientific validation here """
                
                """ creation date -> jd + duree """
                
                ee = RoutineRequest()
                eee = ee.getByID(id)
                
                eee.update(
                    name = request.POST['name'],
                    laboratory = request.POST['laboratory'],
                    telnumber = request.POST['telnumber'],
                    email = request.POST['email'],
                    creation_date = request.POST['creation_date'],
                    request_is_ALERT = (True if request.POST['request_is_ALERT']==True else False),
                    seq_number = int(request.POST['seq_number']),        
                        
                        )                   
                 
                template = loader.get_template('routinemanager/index.html')                    
                success = True
                context = RequestContext(request, {      
                    'form' : form,                                          
                    'success' : success,       
                })
            
                return HttpResponse(template.render(context))
            else:
                e = 1
                return render_to_response('routinemanager/edit.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    except:   
        e = 2
        return render_to_response('routinemanager/edit.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
                
                

   



