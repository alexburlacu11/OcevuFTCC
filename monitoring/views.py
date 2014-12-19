


# this is the defaul function called when invoking the monitoring
# it creates 2 watchers, calls their function by polymorphism
# then saves the results in the database
# The monitoring loop does not necessarily have to run
# in order to request info about the watchers

from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(self):
    #returns watcher conditions from monitoring database (boolean values)
    #monitoring = Guardian.objects.first()
    html = "<html><body>Guardian status: </br>%s.</body></html>"# % monitoring.to_string()
    return HttpResponse(html)
        
