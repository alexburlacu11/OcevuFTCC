


# this is the defaul function called when invoking the guardian
# it creates 2 watchers, calls their function by polymorphism
# then saves the results in the database
# The guardian loop does not necessarily have to run
# in order to request info about the watchers

from django.shortcuts import render

def index(self):
    #returns watcher conditions from guardian database (boolean values)
    guardian = Guardian.objects.first()
    html = "<html><body>Guardian status: </br>%s.</body></html>"# % guardian.to_string()
    return HttpResponse(html)
        
def status(self):
    #returns watcher values from their respective tables
    weather = Weather.objects.first()
    site = Site.objects.first()
    security = Security.objects.first()
    
def history(self):
    guardian = Guardian.objects.all()