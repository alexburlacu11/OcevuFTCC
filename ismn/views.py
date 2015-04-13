import json

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from ismn.admin import UserCreationForm, UserChangeForm
from common.models import OFTThreadManager

from ismn.models import MyUserManager


# from forms import RegistrationForm, LoginForm
# @accept_websocket
# def consoleOutput(request):
#     if not request.is_websocket():
#         
#         print "bad shit"
#         
#         result = OFTThreadManager.getConsoleOutput()  
#   
#         if result == None or result == "":
#             result = 'No data received' 
#         data = ( {'c1':result[0] , 'c2':result[1] })
#     
#         convertedJSON = json.dumps(data, ensure_ascii=False)   
#     
#         return HttpResponse(convertedJSON)
#     
#     else:
#         
#         print "good shit"
#         
#         for i in xrange(0,10):
#            
#             request.websocket.send(i)
# Create your views here.
# def console(request):
#     """redirect to console page"""
#     template = loader.get_template('ismn/console.html')
#     context = RequestContext(request, {          
#                 
#     })
#     return HttpResponse(template.render(context))
#     return redirect('http://localhost:8001/', permanent=True)
# def consoleOutput_ORIGINAL(request):
#     result = OFTThreadManager.getConsoleOutput()  
#   
#     if result == None or result == "":
#         result = 'No data received' 
#     data = ( {'c1':result[0] , 'c2':result[1] })
# 
#     convertedJSON = json.dumps(data, ensure_ascii=False)   
# 
#     return HttpResponse(convertedJSON)
def index(request):
    """redirect to index page for logging in"""
    state = "Please log in or create a new account."
    template = loader.get_template('ismn/index.html')    
    
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,  
        
    })

    return HttpResponse(template.render(context))

def new_user(request):
    """redirect to page for creation of a new user"""
    state = "Submit your request for account creation"
    registrationform = UserCreationForm()
    template = loader.get_template('ismn/new_user.html')        
    context = RequestContext(request, {          
        'info': "info",  
        'form': registrationform,     
        'state':state, 
    })

    return HttpResponse(template.render(context))

def profile(request):
    """view the profile of the user"""
    
    form = UserChangeForm(instance=request.user)
    
    template = loader.get_template('ismn/profile.html')        
    context = RequestContext(request, {          
        'form':form
    })

    return HttpResponse(template.render(context))


def create(request):
    
    """create a user"""
       
    registrationform = UserCreationForm(request.POST)
    if request.POST:
           
            if registrationform.is_valid():
                    registrationform.save() 
                    template = loader.get_template('ismn/index.html')
                    state = "Account creation successful ! Login to continue"                   
                    context = RequestContext(request, { 'state':state, 'info':'ok'})   
                             
                    return HttpResponse(template.render(context))                
            else:
                    state = "One or more fields contain errors. Please try again"    

    else:
          state = "The system encountered an error. Please try again"    

    template = loader.get_template('ismn/new_user.html')
    context = RequestContext(request, 
            {
             'state':state, 
             'error':"error",              
             'form': registrationform             
             }) 
               
    return HttpResponse(template.render(context))    
   
def updateSequenceForConditions(request):
    
    """updateSequenceForConditions a user profile"""
       
    form = UserChangeForm(request.POST)
    if request.POST:           
            if form.is_valid():     
                                  
                    user = form.save() 
                    logout(request)                     
                    
                    state = "Modifications successful, please login in order for changes to take effect"
                    template = loader.get_template('ismn/index.html')    
                    registrationform = UserCreationForm()
                    context = RequestContext(request, {          
                        'info': "info",  
                        'state':state,  
                        'form': registrationform,          
                    })
                
                    return HttpResponse(template.render(context))            
            else:
                    state = "One or more fields contain errors. Please try again"    

    else:
          state = "The system encountered an error. Please try again"    

    template = loader.get_template('ismn/profile.html')
    context = RequestContext(request, 
            {
             'state':state, 
             'error':"error",              
             'form': form             
             }) 
               
    return HttpResponse(template.render(context)) 


def login_user(request):

    """login a user""" 
       
    username = password = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')       
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:                
                login(request, user)
                request.session['user'] = email
                state = "You have successfully logged in, Welcome !"
                template = loader.get_template('ismn/main.html')
                context = RequestContext(request, { 'state':state, 'success':'success'})            
                return HttpResponse(template.render(context))                
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your email and/or password were incorrect."

    template = loader.get_template('ismn/index.html')
    context = RequestContext(request, 
            {
             'state':state, 
             'error':"error", 
             'email':email,             
             })            
    return HttpResponse(template.render(context))    



def main(request):
    """ismn home page redirect """
    template = loader.get_template('ismn/main.html')
    context = RequestContext(request, {  }) 
    return HttpResponse(template.render(context))



def logout_user(request):
    """logout a user"""
    logout(request)
    state = "Logout successful !"
    template = loader.get_template('ismn/index.html')    
    registrationform = UserCreationForm()
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,  
        'form': registrationform,          
    })

    return HttpResponse(template.render(context))

def dashboard(request):
    return redirect('http://localhost:8001')

def voevent_viewer(request):
    return redirect('http://localhost:8002')

    
    