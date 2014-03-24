from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
#     get VOEVENT and send it to page

    template = loader.get_template('voeventtemplate.html')
    a = 10
    context = RequestContext(request, {
        'a': a,
        
    })
    
    return HttpResponse(template.render(context))