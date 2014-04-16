from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

#QUE DE L AFFICHAGE formattage dans la vue, le model recupere des donnees, recuperation et enregistrement

from django.core.urlresolvers import reverse

from forms import DocumentForm
from models import Document
from models import Alert
from forms import AlertForm


def loadfromfile(request):
    """redirect to loadfromfile page """
        
    template = loader.get_template('alertmanager/loadfromfile.html')
    form = DocumentForm()
    context = RequestContext(request, {          
        'form': form, 
    })

    return HttpResponse(template.render(context))

def add(request):
    """redirect to add page """
    
    template = loader.get_template('alertmanager/add.html')    
    alert_form = AlertForm()
    context = RequestContext(request, {          
        'form':alert_form, 
    })

    return HttpResponse(template.render(context))

def alert_to_db(request):
    """insert alert in database"""
    
    try:
        if request.method == 'POST':
            form = AlertForm(request.POST)
#             ee = Alert()
#             eee = ee.getByIvorn(request.POST['ivorn'])
            if form.is_valid():
#                 if (eee):                
#                     alert = Alert(id = eee.id, ivorn = request.POST['ivorn'], role = request.POST['role'], author = request.POST['author'], )
#                 else:
#                     alert = Alert(ivorn = request.POST['ivorn'], role = request.POST['role'], author = request.POST['author'], )                   
               
                """ scientific validation here """
                alert = Alert(ivorn = request.POST['ivorn'], role = request.POST['role'], author = request.POST['author'], )                   
               
                                
                alert.save()    
                template = loader.get_template('alertmanager/index.html')                    
                success = True
                context = RequestContext(request, {      
                    'form' : form,                                          
                    'success' : success,       
                })
            
                return HttpResponse(template.render(context))
            else:
                e = 1
                return render_to_response('alertmanager/add.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    except:   
        e = 2
        form2 = AlertForm(request.POST)
        return render_to_response('alertmanager/add.html', {'form': form2, 'error': e, }, context_instance=RequestContext(request))
        
def update_to_db(request):
    """update alert in database"""
    
    try:
        if request.method == 'POST':
            form = AlertForm(request.POST)
            id = request.POST['id']
            if form.is_valid():

                """ scientific validation here """
                
                ee = Alert()
                eee = ee.getByID(id)
                
                eee.update(ivorn = request.POST['ivorn'], role = request.POST['role'], author = request.POST['author'], )                   
                 
                template = loader.get_template('alertmanager/index.html')                    
                success = True
                context = RequestContext(request, {      
                    'form' : form,                                          
                    'success' : success,       
                })
            
                return HttpResponse(template.render(context))
            else:
                e = 1
                return render_to_response('alertmanager/edit.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    except:   
        e = 2
        form2 = AlertForm(request.POST)
        return render_to_response('alertmanager/edit.html', {'form': form2, 'error': e, }, context_instance=RequestContext(request))
                
        

def list(request):
    """redirect to list page """
      
    template = loader.get_template('alertmanager/list.html')
    ev = Alert()
    events = ev.getAll()    
    context = RequestContext(request, { 
        'events': events,  
    })

    return HttpResponse(template.render(context))

def edit(request):
    """redirect to edit page """
    id = request.POST['id'] 
    template = loader.get_template('alertmanager/edit.html')
    ev = Alert()
    event = ev.get(id)
    
    """ do editing here """
    
    form = AlertForm(instance=event)    
        
    context = RequestContext(request, {          
        'form' : form,
        'id' : id
    })

    return HttpResponse(template.render(context))

def delete(request):
    """ redirect to main page """
    id = request.POST['id'] 
    template = loader.get_template('alertmanager/index.html')
    ev2 = Alert()
    evv = ev2.get(id)
    evv.delete()
    ev = Alert()
    events = ev.getAll()
    success = True
    context = RequestContext(request, {  
        'events': events,  
        'success_delete' : success,
    })
    
    return HttpResponse(template.render(context))


def view(request):
#     get VOEVENT and send it to page
    id = request.POST['id'] 
    template = loader.get_template('alertmanager/view.html')
    ev = Alert()
    event = ev.get(id)
    context = RequestContext(request, {          
        'a':event, 
        'id':id,
    })

    return HttpResponse(template.render(context))



def upload_file(request):
    """upload voevent to the server for analysis"""
    ev = Alert()
    myevents = ev.getAll()
    form = DocumentForm(request.POST, request.FILES)    
    # Handle file upload
    try:
        if request.method == 'POST':
            
            if form.is_valid():
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.save()    
                filename = request.FILES['docfile'].name
                template = loader.get_template('alertmanager/voeventviewer.html')    
                v = Alert()
                data = v.loadVOEventFromXML("documents/"+filename)            
                context = RequestContext(request, {                  
                    'a': data,      
                })
            
                return HttpResponse(template.render(context))
            else:
                e = 1
                return render_to_response('alertmanager/loadfromfile.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    except:   
        e = 2
           
        return render_to_response('alertmanager/loadfromfile.html', {'form': form, 'error': e, }, context_instance=RequestContext(request))
        
    
    
    
def index(request):
    """main index page of alert manager"""
    template = loader.get_template('alertmanager/index.html') 
   
    context = RequestContext(request, {          
    
    })

    return HttpResponse(template.render(context))

   



