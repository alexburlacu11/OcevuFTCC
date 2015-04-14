
from django.http import HttpResponse
from django.template import RequestContext, loader
from planner.models import Sequence, Planning, Owner, Quota, PlanningHistory
from django.contrib.auth.decorators import login_required

 
@login_required
def index(request):
    """redirect to index page """
    template = loader.get_template('planner/index.html')
    plannings = len(PlanningHistory.objects.all()) 
    nr_of_seq = len(Sequence.objects.all())
    context = RequestContext(request, {          
        'nr_of_plannings': plannings, 
        'nr_of_seq': nr_of_seq,
    })
 
    return HttpResponse(template.render(context))


def run(request):
    planning = Planning( 0.0, [] , 0.0, 0.0, 0.0, 0.0)
    planStart = 2456945.18
    planEnd =   2456945.99
    owner1 = Owner(name="John", affiliation='France', priority=60)
    owner1.save()
    quota1 = Quota(owner=owner1, quotaNightLeft=60, quotaNightTotal=100)
    quota1.save()
    planning.initFromCador(owner1, quota1)    
    planning.initFromDB(planStart, planEnd)
    planning.schedule()
    return planning
    
def viewCurrentPlanning(request):
    planning = run(request)
    template = loader.get_template('planner/planning.html')
    sequences = list(Sequence.objects.all()) 
    context = RequestContext(request, {          
        'object_list': sequences,   
        'planning': planning     
    })
   
    return HttpResponse(template.render(context))

def viewOlderPlanning(request, idPlan):
    template = loader.get_template('planner/planning.html')
    planning = PlanningHistory.objects.get(id=idPlan)
    seqs1 = planning.sequences
    seqs2 = seqs1.strip().strip('[').strip(']').split(",")
    sequences = []
    for i in seqs2:
        s = Sequence.objects.get(id=long(i))
#         s.TSP = s.jd2gd(float(s.TSP))
#         s.TEP = s.jd2gd(float(s.TEP))
        sequences.append(s) 
    context = RequestContext(request, {          
        'object_list': sequences,  
        'planning': planning
    })
 
    return HttpResponse(template.render(context))

def getOlderPlannings(request):
    template = loader.get_template('planner/older_plannings_list.html')
    plannings = list(PlanningHistory.objects.all())  
    context = RequestContext(request, {          
        'object_list': plannings,        
    })
 
    return HttpResponse(template.render(context))
