
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Sequence, Planning, Owner, Quota
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """redirect to index page """
         
    template = loader.get_template('planner/index.html')
    
    planning = Planning( 0.0, [] , 0.0, 0.0, 0.0, 0.0)
    planStart = 2456919.18
    planEnd =   2456919.99
    owner1 = Owner(name="John", affiliation='France', priority=60)
    owner1.save()
    quota1 = Quota(owner=owner1, quotaTotal=100, quotaRemaining=60)
    quota1.save()
    planning.initFromCador(owner1, quota1)    
    planning.initFromDB(planStart, planEnd)
    planning.schedule()

    object_list = planning.sequencesHistory[len(planning.sequencesHistory)-1]
    context = RequestContext(request, {          
        'object_list': object_list, 
    })
 
    return HttpResponse(template.render(context))
