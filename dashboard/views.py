from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
# from forms import RegistrationForm, LoginForm
from admin import UserCreationForm, UserChangeForm
from django.core.urlresolvers import reverse
from models import MyUserManager

# Create your views here.
def index(request):
    """redirect to index page for logging in"""
    state = "Please log in or create a new account."
    template = loader.get_template('dashboard/index.html')    
    
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,  
        
    })

    return HttpResponse(template.render(context))

def new_user(request):
    """redirect to page for creation of a new user"""
    state = "Submit your request for account creation"
    registrationform = UserCreationForm()
    template = loader.get_template('dashboard/new_user.html')        
    context = RequestContext(request, {          
        'info': "info",  
        'form': registrationform,     
        'state':state, 
    })

    return HttpResponse(template.render(context))

def profile(request):
    """view the profile of the user"""
    
    form = UserChangeForm(instance=request.user)
    
    template = loader.get_template('dashboard/profile.html')        
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
                    template = loader.get_template('dashboard/index.html')
                    state = "Account creation successful ! Login to continue"                   
                    context = RequestContext(request, { 'state':state, 'info':'ok'})   
                             
                    return HttpResponse(template.render(context))                
            else:
                    state = "One or more fields contain errors. Please try again"    

    else:
          state = "The system encountered an error. Please try again"    

    template = loader.get_template('dashboard/new_user.html')
    context = RequestContext(request, 
            {
             'state':state, 
             'error':"error",              
             'form': registrationform             
             }) 
               
    return HttpResponse(template.render(context))    
   
def update(request):
    
    """update a user profile"""
       
    form = UserChangeForm(request.POST)
    if request.POST:           
            if form.is_valid():     
                                  
                    user = form.save() 
                    logout(request)                     
                    
                    state = "Modifications successful, please login in order for changes to take effect"
                    template = loader.get_template('dashboard/index.html')    
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

    template = loader.get_template('dashboard/profile.html')
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
                template = loader.get_template('dashboard/main.html')
                context = RequestContext(request, { 'state':state, 'success':'success'})            
                return HttpResponse(template.render(context))                
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your email and/or password were incorrect."

    template = loader.get_template('dashboard/index.html')
    context = RequestContext(request, 
            {
             'state':state, 
             'error':"error", 
             'email':email,             
             })            
    return HttpResponse(template.render(context))    



def main(request):
     """dashboard home page redirect """
     template = loader.get_template('dashboard/main.html')
     context = RequestContext(request, {  }) 
     return HttpResponse(template.render(context))



def logout_user(request):
    """logout a user"""
    logout(request)
    state = "Logout successful !"
    template = loader.get_template('dashboard/index.html')    
    registrationform = UserCreationForm()
    context = RequestContext(request, {          
        'info': "info",  
        'state':state,  
        'form': registrationform,          
    })

    return HttpResponse(template.render(context))

    
    