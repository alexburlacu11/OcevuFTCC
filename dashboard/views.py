from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from forms import RegistrationForm, LoginForm

from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    loginform = LoginForm()
    registrationform = RegistrationForm()
    state = "Please log in or create a new account."
    template = loader.get_template('dashboard/index.html')    
    
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,        
    })

    return HttpResponse(template.render(context))


def login_user(request):
    title = "Welcome to the Ocevu Fast Telescope Control Center"
    
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = username
                state = "You're successfully logged in!"
                template = loader.get_template('dashboard/main.html')
                context = RequestContext(request, { 'state':state  })            
                return HttpResponse(template.render(context))                
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    template = loader.get_template('dashboard/index.html')
    context = RequestContext(request, {'state':state, 'error':"error", 'username':username})            
    return HttpResponse(template.render(context))    



def main(request):
     template = loader.get_template('dashboard/main.html')
     context = RequestContext(request, {  }) 
     return HttpResponse(template.render(context))



def logout_user(request):
    logout(request)
    state = "Please log in or create a new account."
    template = loader.get_template('dashboard/index.html')    
    
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,        
    })

    return HttpResponse(template.render(context))

    
    