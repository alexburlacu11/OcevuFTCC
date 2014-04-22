from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

#QUE DE L AFFICHAGE formattage dans la vue, le model recupere des donnees, recuperation et enregistrement

from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
#     get VOEVENT and send it to page
    template = loader.get_template('dashboard/index.html')    
    title = "Welcome to the Ocevu Fast Telescope Control Center"
    context = RequestContext(request, {          
        'title': title,      
    })

    return HttpResponse(template.render(context))
