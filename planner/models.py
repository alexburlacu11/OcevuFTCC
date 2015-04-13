# Create your models here.
'''
Created on Jul 7, 2014

@author: alex
'''


""" 
priority: 0
          1 .. 10 alerts
          10 ... 100 routines
          
parameter : 5 seconds delay between plannifications

1st planning midi solaire 
    
quota affiliation : fr / mx 50 % de temps restant sauf pour les alerts

add to dashboard configuration for quota

delta_time : delay after manual interrupt 6000s 

jd2 = jd2 - duree

immediate : jd2 inconnu et jd1 connu
 jd1O et jd2O inclus dans jd1 jd2
 jd2O indetermine -> jd1O fixe
 add to form jd1Owner and jd2OWner to form. if they are not inside the interval of jd1 et jd2 fournis par ./astro
 then validation error. If no jd2 is chosen, just take in consideration the jd1
 visibility interval vs chosen interval . Add a small interrogation point which explains if no jd2 chosen then take jd1
 add a start for required in jd1 
 
 jd2O - jd1O >= duree
 jd2 - jd1O >= duree
 
 
add the 3 horologes toulouse mexic tijuana, le temps universel ,  in the request form wizard

add jd1 et jd2 de ./astro comme interval maximale de visibilite.
        where we do not have a jd2Owner, create one by adding jd2Owner = jd1Owner + duration <= jd2 
        
1 julian second = 0.00001157401129603386

"""

"""
            order sequences
            1. reprise de quota
            2. garde la sequence en cours, prend le jd2
            3. recommence avec les sequences eligibles
            4. add the end of the day create a history of the day plannification and restart from scratch.
               keep executed sequences in the day's planning but when the day ends put them in a history and delete
               everything               
               point 3:
                   order by priority
                   order by JD2              
                   
        
        
        message : le best eleve n est pas entre jd1 et jd2 show on the web page
        
        sequence plus prioritaires, et on elimine les sequences qui ne sont plus observables et les sequences dejq planned . on attend le fin 
        de l executor de sequence en cours si c est une seq,  sauf si c est une alerte
        
        on atetnds 5 seconds at least from the last req inserted
        
        
        input -> test output tdp = x tep = y
        
        
        todo:
        read seq and put in db
        schedule
        updateSequenceForConditions sequences in db
        view seq verticale on web
        sequences complexe tests with decallage
         
"""


import matplotlib.pyplot as plt 
import matplotlib.dates as dates
from operator import itemgetter, attrgetter
from matplotlib.ticker import FormatStrFormatter 
from django.db import models
import operator
import copy 
import urllib.request as urllib2 
from decimal import *
from common.models import Agent
import datetime

JULIAN_SECOND = 115740
PRECISION = 8

from HTMLParser import HTMLParser 

class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = [] 
    
    def handle_data(self, data):
        self.data.append(data)
        

class Owner(models.Model):
    name = models.CharField(max_length="20", default="Alex")
    affiliation = models.CharField(max_length="20", default="Fr")
    priority = models.IntegerField(default=12)
            
class Quota(models.Model):
    owner = models.ForeignKey(Owner)
    quotaNightLeft = models.IntegerField(default=-1)
    quotaNightTotal = models.IntegerField(default=-1)
        
    def addQuota(self, val ):
        self.quotaNightLeft += val
        
    def substractQuota(self, val):
        self.quotaNightLeft -= val
         
        
class Interval:
    def __init__(self, start, end, duration):
        """Convert to decimal because django uses DecimalField. A FloatField is not enough"""
        self.start = Decimal(start)
        self.end = Decimal(end)
        self.duration = Decimal(duration)
   
    def display(self):
        print( "["+str(self.start)+" - "+str(self.end)+"]")     
 
class PlanningHistory(models.Model): 
    id = models.AutoField(primary_key=True)
    sequences = models.TextField("Sequences")
    planStart = models.DecimalField(default=0.0, max_digits=15, decimal_places=8)
    planEnd = models.DecimalField(default=0.0, max_digits=15, decimal_places=8)
    creationDate = models.DateTimeField(auto_now_add=True, blank=True,)       
        
class Sequence(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(Owner)
    jd1Owner = models.DecimalField(default=0.0, max_digits=15, decimal_places=8)
    jd2Owner = models.DecimalField(default=0.0, max_digits=15, decimal_places=8)      
    priority = models.IntegerField(default=0)
    duration = models.DecimalField(default=0.0, max_digits=15, decimal_places=8)
    tPrefered = models.DecimalField(default=-1.0, max_digits=15, decimal_places=8)   #temps en seconds compris entre jd1Owner et jd2Owner      
    status = models.CharField(max_length="21", default="SUBMITTED")
    TSP = models.DecimalField(default=-1.0, max_digits=15, decimal_places=8)
    TEP = models.DecimalField(default=-1.0, max_digits=15, decimal_places=8)
    deltaTL = models.DecimalField(default=-1.0, max_digits=15, decimal_places=8) 
    deltaTR = models.DecimalField(default=-1.0, max_digits=15, decimal_places=8)
    darkness = models.DecimalField(default=-1.0, max_digits=15, decimal_places=2)
    seeing = models.DecimalField(default=-1.0, max_digits=15, decimal_places=2)
    rain = models.DecimalField(default=-1.0, max_digits=15, decimal_places=2)
    clouds = models.DecimalField(default=-1.0, max_digits=15, decimal_places=2)
    
        
    def display(self):
        print( "["+str(datetime.datetime.now())+"]"+"Seq:"+str(self.id)+" TSP:"+str(self.TSP)+" TEP:"+str(self.TEP)+" tPref:"+str(self.tPrefered)+" duration:"+str(self.duration)+" jd1Owner:"+str(self.jd1Owner)+" j2Owner:"+str(self.jd2Owner)+" shiftLeft:"+str(self.deltaTL)+" shiftRight:"+str(self.deltaTR)+" priority:"+str(self.priority)+" status:"+str(self.status))
     
    def gd2jd(self, datestr):
        """ Convert a string Gregorian date into a Julian date using Pylab.
            If no time is given (i.e., only a date), then noon is assumed.
            Times given are assumed to be UTC (Greenwich Mean Time).
    
           EXAMPLES:
                print( "["+str(datetime.datetime.now())+"]"+gd2jd('Aug 11 2007')   ---------------> 2454324.5
                print( "["+str(datetime.datetime.now())+"]"+gd2jd('12:00 PM, January 1, 2000')  --> 2451545.0
    
           SEE ALSO: jd2gd
           """
        # 2008-08-26 14:03 IJC: Created        
        
        if datestr.__class__==str:
            d = dates.datestr2num(datestr)
            jd = dates.num2julian(d) + 3442850
        else:
            jd = []
    
        return jd

                
    def jd2gd(self, juldat):
        """ Convert a numerial Julian date into a Gregorian date using Pylab.
            Timezone returned will be UTC.
    
           EXAMPLES:
              print( "["+str(datetime.datetime.now())+"]"+jd2gd(2454324.5)  --> 2007-08-12 00:00:00
              print( "["+str(datetime.datetime.now())+"]"+jd2gd(2451545)    --> 2000-01-01 12:00:00
    
           SEE ALSO: gd2jd"""
        # 2008-08-26 14:03 IJC: Created    
        d = dates.julian2num(juldat)
        gd = dates.num2date(d - 3442850)
    
        return gd
          
        
class SequenceOrder(models.Model):                
    id = models.AutoField(primary_key=True)
    sequence = models.ForeignKey(Sequence)
    
class PlanningController(Agent):
    
    def __init__(self):
        Agent.__init__(self, 'Planning')
        self.planning = Planning( 0, [] , 0, 0, 0, 0)
        
    def updateWithNewSequences(self, planStart, planEnd):
        sequences = list(Sequence.objects.filter(jd1Owner__gte=planStart).filter(jd2Owner__lte=planEnd)) 
        for seq in sequences:
#             seq.display()
            seq.status = "TOBEPLANNED" 
            seq.save()
    
    def work(self):
        """TO DO register with monitoring controller at 18:00"""
        
        planStart = 2456981.68
        planEnd = 2456981.76     
        
#         self.generateFakeSequences()

        self.updateWithNewSequences(planStart, planEnd)
              
        self.planning.initFromDB(planStart, planEnd)
        self.planning.schedule()
        self.planning.displaySimple()
        self.registerTo("Monitoring")
        self.registerTo("AlertManager")
        self.registerTo("RoutineManager")
        """ 
            during day -> observable -> first plannification
            planning controller prends certains observables et planned-> pass to tobeplanned si il y a eu un passage
            replan
            
            at a precise hour 
            
        """
    
    def generateFakeSequences(self):
        Sequence.objects.all().delete()
        owner = Owner()
        owner.save()
        idSeq = 1                       
        jd1Owner = 2456981.68341667
        jd2Owner = 2456981.73684001
        duration = jd2Owner-jd1Owner
        priority = 10
        darkness = 11
        sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration, darkness=darkness)
        sequence.save()
        idSeq = 2                       
        jd1Owner = 2456981.74117667
        jd2Owner = 2456981.75684001
        duration = jd2Owner-jd1Owner
        priority = 10
        darkness = 12
        sequence1 = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration, darkness=darkness)
        sequence1.save()         
   
    def analyseMessage(self, conn, data):
        
#         print( "["+str(datetime.datetime.now())+"]"+"Planning controller received : "+data
#         
#         data = data.rstrip('\n')
        
        """This is to pass from submitted to TOBEPLANNED"""
        self.updateWithNewSequences(self.planning.planStart, self.planning.planEnd)
        
        
        if data == "start" or data == "plan":
            """normally get all sequences from db which are to be planned and pass them o observable if conditions are good"""
            self.work()                        
        else: 
            if data == "stop":
                Agent.analyseMessage(self, data)                
            else:
                """ the alert and routine case """ 
                if data == "alert":
                    print( "["+str(datetime.datetime.now())+"]"+"Alert has been received,  interrupting and replanning " )
                    dataSet=["Darkness", 20]                   
                    ok = self.updateSequenceForConditions(dataSet)
                    if ok == True:
                        self.planning.reschedule(self.planning.planStart)
                        self.planning.displaySimple()
                    """ TODO : add logic for interrupting observation system and replan after""" 
                else:
                    if data == "request":
                        print( "["+str(datetime.datetime.now())+"]"+"Request has been received, don't interrupt anything but replan")
                        dataSet=["Darkness", 20]                   
                        ok = self.updateSequenceForConditions(dataSet)
                        if ok == True:
                            self.planning.reschedule(self.planning.planStart)
                            self.planning.displaySimple()
                    else:
                        dataSet = data.split(":")
                        parameterName = dataSet[0]
                        parameterCurrentValue = dataSet[1]
#                         print( "["+str(datetime.datetime.now())+"]"+str(parameterName)+":"+str(parameterCurrentValue)
                        ok = self.updateSequenceForConditions(dataSet)
                        if ok == True:
                            self.planning.reschedule(self.planning.planStart)
                            self.planning.displaySimple()
        conn.send(bytes("ok", 'UTF-8'))
    
    def updateSequenceForConditions(self, dataSet):
        """if function returns True then reschedule, else do nothing"""        
        sequencesPlanned = list(Sequence.objects.filter(status="PLANNED"))
        sequencesObservable = list(Sequence.objects.filter(status="OBSERVABLE"))
        sequencesTobeplanned = list(Sequence.objects.filter(status="TOBEPLANNED"))        
        sequences = sequencesPlanned + sequencesObservable + sequencesTobeplanned
        mustReplan = False
        for seq in sequences:
            """if conditions have not changed, checkConditions returns false, else true"""
            changeStatusFlag = self.checkConditions(seq, dataSet)
            if changeStatusFlag and seq.status == "PLANNED" or seq.status == "OBSERVABLE":
                seq.status = "TOBEPLANNED" 
                seq.save()
                mustReplan = True
            else:
                if changeStatusFlag and seq.status == "TOBEPLANNED":
                    seq.status = "OBSERVABLE"
                    seq.save()
                    mustReplan = True
                
        self.planning.sequences = Sequence.objects.filter(status="PLANNED").filter(status="OBSERVABLE").filter(status="TOBEPLANNED")
        """ if there are no sequences that changed, there is no need to replan so return false, else replan"""
              
        return mustReplan
        
                
    def checkConditions(self, seq, dataSet):
        """checks to see if observation conditions are ok, if they are not, then a status change is needed so return true"""
        parameterName = dataSet[0]
        parameterCurrentValue = dataSet[1]
        if seq.darkness <= float(parameterCurrentValue):
            """change because seq needs a higher darkness"""
            return True
        else:
            return False
        
        
        
        
class Planning:
    def __init__(self, mode, sequences, currentSequence, currentTime, planStart, planEnd, ):
        """mode 1 classic entre 2 journees de planification, 2 cas alerte, 3 request, 4 apres alarme""" 
        planStart = float(planStart)
        planEnd = float(planEnd)
        self.mode = mode
        self.sequences = sequences
        self.currentSequence = currentSequence
        self.currentTime = currentTime               
        self.intervals = [Interval(planStart, planEnd, planEnd-planStart),]
        self.sequencesHistory = {}
    
           
    def initFromMemory(self, sequences, planStart, planEnd): 
        self.planStart = float(planStart)
        self.planEnd = float(planEnd)
        self.mode = "DEBUG"
        self.sequences = sequences
        self.intervals = [Interval(planStart, planEnd, planEnd-planStart) ,]
#         self.currentSequence = sequences[0]
#         self.currentTime = 1
        
    def initFromDB(self, planStart, planEnd):        
        sequences = list(Sequence.objects.filter(status="OBSERVABLE")) 
        self.initFromMemory(sequences, planStart, planEnd)
        
    def initFromCadorFile(self, owner, quota):
        """this function loads the latest sequences from CADOR and uses them in planning"""
#         response = urllib2.urlopen('E:\\a.htm')
        with open ("E:\\a.htm", "r") as myfile:
            data=myfile.read()
#         data = response.read()
        parser = MyHTMLParser()
        parser.feed(data) 
              
        """filter unwanted \n and other data"""
        filteredList = map(lambda s: s.strip(), parser.data)
        pageText = filteredList[9]
        print( "["+str(datetime.datetime.now())+"]"+pageText )
        rawSequences = pageText.split("\n")
        del rawSequences[0]
        """Create the sequences"""
        for rawSequence in rawSequences:
            sequenceArray = rawSequence.split(" ")
#             day = int(sequenceArray[5].split(".")[0])
#             if day >= 2456910 and day <= 2456911:
            idSeq = int(sequenceArray[0])                       
            jd1Owner = "%.8f" % float(sequenceArray[5])
            jd2Owner = "%.8f" % float(sequenceArray[6])
            duration = (float(sequenceArray[4])/86400.0)
            priority = int(sequenceArray[2])
            sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration)
            sequence.save()
#             sequence.display()
        
    def initFromCador(self, owner, quota):
        """this function loads the latest sequences from CADOR and uses them in planning"""
        response = urllib2.urlopen('http://cador.obs-hp.fr/ros/scenes_cador.php/') 
        data = response.read()
        parser = MyHTMLParser()
        parser.feed(data)       
        """filter unwanted \n and other data"""
        filteredList = map(lambda s: s.strip(), parser.data)
        pageText = filteredList[10]
        rawSequences = pageText.split("\n")
        del rawSequences[0]
        """Create the sequences"""
        for rawSequence in rawSequences:
            sequenceArray = rawSequence.split(" ")
#             day = int(sequenceArray[5].split(".")[0])
#             if day >= 2456910 and day <= 2456911:
            idSeq = int(sequenceArray[0])                       
            jd1Owner = "%.8f" % float(sequenceArray[5])
            jd2Owner = "%.8f" % float(sequenceArray[6])
            duration = (float(sequenceArray[4])/86400.0)
            priority = int(sequenceArray[2])
            sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration)
            sequence.save()
#             sequence.display()

    def getPlanningSequenceIDs(self):
        """ returned planned sequences from db """
        return [int(seq.id) for seq in self.sequences if seq.status=="PLANNED" or seq.status=="FIXED"]
    
    def getFillingRate(self):
        """get the free space in the planning""" 
        totalDuration = self.planEnd - self.planStart        
        filledDuration = sum([seq.duration for seq in self.sequences if seq.status == "PLANNED"])
        return filledDuration * Decimal(100.0) / Decimal(totalDuration)
        
    def getKlotzSequenceIDs(self):
        """this function loads the latest sequences from CADOR PLANNING and compares them with my plannification"""
        listReturned = []
        response = urllib2.urlopen('http://cador.obs-hp.fr/ros/sequenced1.txt')
        data = response.read()
        parser = MyHTMLParser()
        parser.feed(data)       
        """filter unwanted \n and other data"""
        filteredList = map(lambda s: s.strip(), parser.data)
        pageText = filteredList[0]    
        rawSequences = pageText.split("\n")  
        """Create the sequences"""
        for i in range(3, len(rawSequences)):
            sequenceArray = rawSequences[i].split(" ")
            matching = [s for s in sequenceArray if "000003" in s]
            if len(matching) == 0:
                break
            else:
                items = matching[0].split("_")
                a = items[0][-1]
                b = items[1][:-2]
                idS = str(a)+str(b)
                listReturned.append(idS)
        return [int(i) for i in listReturned]
        
        
    def initFromFile(self, fileName, owner, quota): 
        with open(fileName, 'r') as f:
#             print( "["+str(datetime.datetime.now())+"]"+"Reading data in file "
            data = f.readlines()
            """remove comments"""
            parsedData1 = [i for i in data if i[0] != '#']
            """remove empty slots like \n"""
            parsedData2 = [i for i in parsedData1 if i != '\n']
            """instantiate objects"""
#             mode = str(parsedData2[0].split('=')[1]).rstrip()
#             planStart = "%.8f" % float(parsedData2[1].split('=')[1])
#             planEnd = "%.8f" % float(parsedData2[2].split('=')[1]) 
            for i in range(3,len(parsedData2)):
                sequenceParameters = parsedData2[i].split(',')
                idSeq = int(sequenceParameters[0])
                """The owner data will be modified accordingly"""
                jd1Owner = "%.8f" % float(sequenceParameters[2])
                jd2Owner = "%.8f" % float(sequenceParameters[3])
                duration = (float(sequenceParameters[4])/86400.0)
                priority = int(sequenceParameters[5])
                sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration)
                sequence.save()
#                 sequence.display()
        f.closed               
                   
    def schedule(self):   
            
        """pre-configuration : initial sorting by priority and jd2Owner"""          
        self.initialSort()
        """loop through sequences which are TOBEPLANNED"""
        instant = 0
        for seq in [sequence for sequence in self.sequences if sequence.status == "OBSERVABLE"]:      
            
            """and try to plan them"""
            if seq.jd1Owner >= self.planStart and seq.jd2Owner <= self.planEnd:
                
                if self.placeSequence(seq):
                    seq.status = "PLANNED" 
                    """save a history of the sequences and their states during the planning"""            
                    if self.mode == "DEBUG":   
                        self.saveInHistory(instant)
                        instant += 1
                else:
                    
                    if (seq.jd2Owner < seq.jd1Owner + seq.duration ) :
                        seq.status = "UNPLANNABLE"
                    
                    else:                        
                        if (float(seq.jd2Owner) == float(seq.jd1Owner) ) :
                            
                            seq.status = "FIXED"               
                        
                        else:
                            
                            seq.status = "OBSERVABLE"               
                
            else:
                if seq.jd1Owner <= self.planStart:
                    seq.status = "UNPLANNABLE"
                else:
                    if seq.jd2Owner >= self.planEnd:
                        seq.status = "SUBMITTED"
                                   
                
            seq.save()
        
        """order the sequences"""
        orderedSequences = sorted(self.sequences, key=attrgetter('TSP'))    
        for seq in orderedSequences:
            sequenceOrder = SequenceOrder(sequence = seq)
            sequenceOrder.save()
            
        """save the planning at the end of the night"""
        sequences = [ seq.id for seq in self.sequences]
        planHistory = PlanningHistory(sequences=sequences, planStart=self.planStart, planEnd=self.planEnd)
        planHistory.save()
        
    def reschedule(self, planStart):
        
        """the function reschedules the planning according to a new planStart"""
        
        self.planStart = planStart
        del self.intervals[:]
        self.intervals.append(Interval(self.planStart, self.planEnd, self.planEnd-self.planStart))
        seqs = list(Sequence.objects.all()) 
        
        for seq in seqs:
            if seq.jd2Owner <= self.planStart and seq.status=="PLANNED":
                seq.status = "EXECUTED" 
                seq.save()       
        
#         for seq in seqs:
#             if seq.status == "PLANNED":
#                 seq.status = "OBSERVABLE" 
#                 seq.save()
        
        self.sequences = list(Sequence.objects.all()) 
        self.schedule()
                           
    def placeSequence(self, seq):
        
        """get indexes list of intervals where the interval duration is > duration of the sequence"""        
        compatibleIntervals = self.filterByDuration(seq) 
               
        if (compatibleIntervals):  
             
            """if there are slots available"""                          
            return self.placeSequenceWithoutShift(compatibleIntervals, seq)
         
        else:
             
            """no slots available, shift to make room"""
            return self.placeSequenceWithShift(seq)
        
                    
    def saveInHistory(self, instant):
        """save a history of the state of the sequences at each instant in the planning"""
        """TODO if debug, make it facultative"""
        currentSequencesInPlanning = [ s for s in self.sequences if s.status == "PLANNED" ]
        self.sequencesHistory[instant] = copy.deepcopy(currentSequencesInPlanning) 
            


    def placeSequenceWithoutShift(self, compatibleIntervals, seq):
        """place the sequence in the planning without relocating other sequences"""
       
        """
        for the list of intervals which have a duration greater than that of the sequence, choose just the one that is between
        jd1Owner and jd2Owner and around tPrefered, if it exists (returns 0 or 1 interval)
        """
        
        preferedIntervals = [interval for interval in compatibleIntervals if seq.tPrefered >= interval.start and seq.tPrefered <= interval.end]        
        
        intervalToBeUsed = preferedIntervals[0] if preferedIntervals else compatibleIntervals[0] 
        Dj = intervalToBeUsed.start
        Fj = intervalToBeUsed.end
        
        ok = False
                   
        if seq.tPrefered == -1.00000000:   
            """this is the case where the user requests immediate observation, meaning tPrefered = -1 """                          
            ok = self.insertSequence("IMMEDIATE", max(intervalToBeUsed.start, seq.jd1Owner), seq)
        else:
            """
                in case of choosing best elevation or between jd1Owner and jd2Owner for the tPrefered, the TSP and
                the TEP will be computed by subtracting and adding the duration accordingly
                TSP will be the tPrefered minus half the duration and TEP will be tPrefered plus the other half of the
                duration
            """
                       
            if preferedIntervals:       
                                                               
                ok = self.insertSequence("MIDDLE", None, seq)
                
                """adjusting TSP and TEP """
                
                if seq.TSP <= max(Dj, seq.jd1Owner):
                    ok = self.insertSequence("LEFT", max(Dj, seq.jd1Owner), seq)                                        
                else:
                    if seq.TEP >= min(Fj, seq.jd2Owner):
                        ok = self.insertSequence("RIGHT", min(Fj, seq.jd2Owner), seq)
                       
            else:
                
                if preferedIntervals is None:
                
                    for interval in compatibleIntervals:
                        if interval.start > seq.tPrefered:
                            ok = self.insertSequence("LEFT", Dj, seq)
                        else:
                            if interval.end < seq.tPrefered:
                                ok = self.insertSequence("RIGHT", Fj, seq)   
                        break      
                       
        """compute the possiblity of shifting the sequences to make room for future sequences"""
        self.computeDeltaTL(Dj, seq)
        self.computeDeltaTR(Fj, seq)
        self.updateIntervals(intervalToBeUsed, seq)
        
        return ok
        
    def placeSequenceWithShift(self, seq):    
        """place the sequence in the largest available interval by shifting previous and/or next sequences"""

        """Look for the largest available interval between jd1Owner and jd2Owner. """
        possibleIntervals = [interval for interval in self.intervals if interval.start >= seq.jd1Owner and interval.end <= seq.jd2Owner]
        longestInterval = Interval(-1,-1,-1)
        if len(possibleIntervals) != 0:
            """get the largest available interval between jd1Owner and jd2Owner"""
            longestInterval = max(self.intervals, key=operator.attrgetter('duration'))
        else:            
            """Abandon sequence, there are no available slots left"""            
            return False
                        
        """Test shift left: search for the sequence which ends at the start of the interval"""        
        resultLeftSequences = [sequence for sequence in self.sequences if sequence.TEP == longestInterval.start]
        if len(resultLeftSequences)!=0:
            sequenceLeft = resultLeftSequences[0]
            if sequenceLeft.deltaTL != 0.0 and seq.duration <= sequenceLeft.deltaTL + longestInterval.duration:            
                    """Shift left sequence"""
    #                 sequenceLeft.display()
                    self.insertSequence("LEFT", sequenceLeft.TSP-sequenceLeft.deltaTL, sequenceLeft)
    #                 self.updateIntervals(largestDurationInterval, sequenceLeft)
                    self.insertSequence("LEFT", sequenceLeft.TEP, seq)
                    self.updateIntervals(longestInterval, seq)                
        else:
            """Try the right side"""
            """Test shift right: search for the sequence which starts in end of interval"""        
            resultRightSequences = [sequence for sequence in self.sequences if sequence.TSP == longestInterval.end]
            if len(resultRightSequences)!=0:
                sequenceRight = resultRightSequences[0]
                if sequenceRight.deltaTR != 0.0 and seq.duration <= sequenceRight.deltaTR + longestInterval.duration:
                    """Try to place the sequence, if it is not enough, it is UNPLANNABLE"""
                    self.insertSequence("LEFT", sequenceRight.TSP + sequenceRight.deltaTR, sequenceRight)
    #                 self.updateIntervals(largestDurationInterval, sequenceRight)
                    self.insertSequence("RIGHT", sequenceRight.TSP, seq)               
                    self.updateIntervals(longestInterval, seq)             
            else:
                """Try to shift to the left first then to the right"""
                if seq.duration <= sequenceRight.deltaTR + sequenceLeft.deltaTL + longestInterval.duration and \
                    sequenceLeft.deltaTL != 0.0 and sequenceRight.deltaTR != 0.0:
                    """Shift left right"""
                    self.insertSequence("LEFT", sequenceLeft.TSP-sequenceLeft.deltaTL, sequenceLeft)
#                     self.updateIntervals(largestDurationInterval, sequenceLeft)
                    self.insertSequence("LEFT", sequenceRight.TSP+sequenceRight.deltaTR, sequenceRight)
#                     self.updateIntervals(largestDurationInterval, sequenceRight)
                    self.insertSequence("LEFT", sequenceLeft.TEP, seq)
                    self.updateIntervals(longestInterval, seq)
                else:
                    return False
                            
        """Update shifts"""
        Dj = longestInterval.start
        Fj = longestInterval.end
        self.computeDeltaTL(Dj, seq)
        self.computeDeltaTR(Fj, seq)
        
        return True
       
    def insertSequence(self, choice, timeInstant, seq,):  
        """insert the sequence at a certain time in the planning"""      
        
        if (choice == "IMMEDIATE"):            
            seq.TSP = timeInstant
            seq.TEP = seq.TSP + seq.duration
            return True
        if (choice == "MIDDLE"):
            seq.TSP = seq.tPrefered-(seq.duration/2)
            seq.TEP = seq.tPrefered+(seq.duration/2)
            return True
        if (choice == "LEFT"):
            seq.TSP = timeInstant
            seq.TEP = seq.TSP + seq.duration
            return True
        if (choice == "RIGHT"):
            seq.TEP = timeInstant
            seq.TSP = seq.TEP - seq.duration
            return True
        
        return False   
        
               
    def initialSort(self):
        """sort in an ascending order according to priority and jd2Owner"""
        """@to do: sort by tPrefered instead of jd2Owner to gain in precision ??"""
        self.sequences.sort(key=lambda x: ( x.priority, x.jd2Owner ), reverse=False)
        
    def filterByDuration(self, seq):
        """ Search for an interval where the duration is > duration of the sequence"""
        longEnoughIntervals = []

        for interval in self.intervals:
            leftLimit = max(interval.start,seq.jd1Owner)
            rightLimit = min(interval.end,seq.jd2Owner)
#             print( "["+str(datetime.datetime.now())+"]"+"interval start and jd1Owner"
#             print( "["+str(datetime.datetime.now())+"]"+interval.start
#             print( "["+str(datetime.datetime.now())+"]"+seq.jd1Owner
#             print( "["+str(datetime.datetime.now())+"]"+leftLimit
#             print( "["+str(datetime.datetime.now())+"]"+"interval end and jd2Owner"
#             print( "["+str(datetime.datetime.now())+"]"+interval.end
#             print( "["+str(datetime.datetime.now())+"]"+seq.jd2Owner
#             print( "["+str(datetime.datetime.now())+"]"+rightLimit
#             print( "["+str(datetime.datetime.now())+"]"+"rightLimit - leftLimit:"
#             print( "["+str(datetime.datetime.now())+"]"+rightLimit - leftLimit
#             print( "["+str(datetime.datetime.now())+"]"+"duration:"
#             print( "["+str(datetime.datetime.now())+"]"+seq.duration
            if rightLimit - leftLimit >= seq.duration:
                longEnoughIntervals.append(interval)
        return longEnoughIntervals

           
    def updateIntervals(self, usedInterval, seq):
        """updateSequenceForConditions new free intervals"""
        intervalBefore = Interval(usedInterval.start, seq.TSP, seq.TSP - usedInterval.start)
        intervalAfter = Interval(seq.TEP, usedInterval.end, usedInterval.end - seq.TEP)
        """remove old interval from the list"""
        self.intervals.remove(usedInterval)
        self.intervals.append(intervalBefore)
        self.intervals.append(intervalAfter)
        if intervalBefore.start >= intervalBefore.end:
            self.intervals.remove(intervalBefore) 
        if intervalAfter.start >= intervalAfter.end:
            self.intervals.remove(intervalAfter)
        self.intervals = sorted(self.intervals, key=lambda interval: interval.start)
       
    def computeDeltaTL(self, Dj, seq):
        """compute the possible value of shifting the sequence to the left"""
        seq.deltaTL = seq.TSP - max(Dj, seq.jd1Owner) #if seq.tPrefered != -1 else 0     
     
    def computeDeltaTR(self, Fj, seq):
        """compute the possible value of shifting the sequence to the right"""
        seq.deltaTR = min(Fj, seq.jd2Owner) - seq.TEP #if seq.tPrefered != -1 else 0
    
                    
    def display(self):       
        """text way of displaying the planning: intervals and sequences"""
        for interval in self.intervals:
            interval.display()            
        for seq in self.sequences:            
            seq.display()
            
        print( "["+str(datetime.datetime.now())+"]"+"\nPLANNED sequences: "+str(len([i for i in self.sequences if i.status == "PLANNED"])))
        print( "["+str(datetime.datetime.now())+"]"+"OBSERVABLE sequences: "+str(len([i for i in self.sequences if i.status == "OBSERVABLE"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOBEPLANNED today sequences: "+str(len([i for i in self.sequences if i.status == "TOBEPLANNED" and i.jd2Owner <= self.planEnd])))
        for i in self.sequences:
            if i.status == "TOBEPLANNED" and i.jd2Owner <= self.planEnd:
                i.display()
        print( "["+str(datetime.datetime.now())+"]"+"TOTAL for today: "+str(len([i for i in self.sequences if i.status == "PLANNED"])+len([i for i in self.sequences if i.status == "TOBEPLANNED" and i.jd2Owner <= self.planEnd])))
        print( "["+str(datetime.datetime.now())+"]"+"UNPLANNABLE sequences: "+str(len([i for i in self.sequences if i.status == "UNPLANNABLE"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOBEPLANNED another night sequences: "+str(len([i for i in self.sequences if i.status == "TOBEPLANNED"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOTAL sequences: "+str(len(self.sequences)))
        print( "["+str(datetime.datetime.now())+"]"+"FILLING RATE: "+str(self.getFillingRate()))
        print( "["+str(datetime.datetime.now())+"]"+"\n")

    def displaySimple(self):
        print( "["+str(datetime.datetime.now())+"]"+"------------------------------------------\n")
        print( "["+str(datetime.datetime.now())+"]"+"PLANNED sequences: "+str(len([i for i in self.sequences if i.status == "PLANNED"])))
        print( "["+str(datetime.datetime.now())+"]"+"OBSERVABLE sequences: "+str(len([i for i in self.sequences if i.status == "OBSERVABLE"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOBEPLANNED today sequences: "+str(len([i for i in self.sequences if i.status == "TOBEPLANNED" and i.jd2Owner <= self.planEnd])))
        print( "["+str(datetime.datetime.now())+"]"+"TOTAL for today: "+str(len([i for i in self.sequences if i.status == "PLANNED"])+len([i for i in self.sequences if i.status == "TOBEPLANNED" and i.jd2Owner <= self.planEnd])))
        print( "["+str(datetime.datetime.now())+"]"+"UNPLANNABLE sequences: "+str(len([i for i in self.sequences if i.status == "UNPLANNABLE"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOBEPLANNED another night sequences: "+str(len([i for i in self.sequences if i.status == "TOBEPLANNED"])))
        print( "["+str(datetime.datetime.now())+"]"+"TOTAL sequences: "+str(len(self.sequences)))
        print( "["+str(datetime.datetime.now())+"]"+"------------------------------------------\n")
            
    def displayGUI(self):
        import numpy as np
        if self.sequences is not None:    
            seqToBePlanned = [seq for seq in self.sequences if seq.status == "PLANNED"]  
            yAxisMin = -0.5
            yAxisMax = len(seqToBePlanned) + 1
            xAxisMin = -1.5
            xAxisMax = self.intervals[len(self.intervals)-1].end
    
            plt.figure(figsize=(30,12), facecolor='orange')
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d')) 
            plt.yticks([a for a in range(0, len(seqToBePlanned)+1)]) 
#             plt.xticks([a for a in xrange(0.0, self.intervals[len(self.intervals)-1].end+1)])            
            plt.xticks(np.arange(self.planStart, self.planEnd, 0.01))
            plt.xticks(rotation='vertical')
            # Pad margins so that markers don't get clipped by the axes
            plt.margins(0.1)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.15)
            plt.grid(True)
            plt.xlabel('Sequences in planing')
            plt.ylabel('Evolution in time') 
            plt.title('Scheduling of sequences in time. Time is computed in using a julian date. We eliminate the integer part and multiply by 10*pow(10)')
            plt.ylim([yAxisMin,yAxisMax])
#             plt.xlim([xAxisMin, xAxisMax])     
            
            
            
            for a in range(0, len(seqToBePlanned)+1):    
                plt.axhline(y=a, xmin=0, xmax=xAxisMax, hold=None, label='free')  
            
            for i in range(0, len(seqToBePlanned)):
                ss = self.sequencesHistory[i]         
                    
                for seq in ss:
                    self.plotSequence(seq, i, plt)
            
            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111)
            
#             ax2.plot(x, z)
 
            for seq in seqToBePlanned:
                self.plotSequence(seq, 1, ax2)
    #         plt.legend()
            plt.show()
        else:
            print( "["+str(datetime.datetime.now())+"]"+"No data available in planning")
        
    def plotSequence(self, seq, y, PLT):      
        
        PLT.plot([seq.TSP, seq.TEP], [y, y], color='r', linestyle='-', linewidth=5, label='Seq'+str(seq.id)+'['+str(seq.TSP)+']['+str(seq.TEP)+']')            
        PLT.plot(seq.TSP, y, marker='o', color='g', linewidth=8)
        PLT.plot(seq.TEP, y, marker='o', color='g', linewidth=8)
#         plt.plot(seq.tPrefered, y, marker='p', color='m', linewidth=8)
        PLT.annotate('seq: '+str(seq.id), xy=((seq.TSP+seq.TEP)/2,y), xytext=(0, 20), ha='center',
            textcoords='offset points')
        PLT.annotate('TSP', xy=(seq.TSP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
        PLT.annotate('TEP', xy=(seq.TEP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
#         plt.annotate('TPref', xy=(seq.tPrefered,y), xytext=(0, -20), ha='center',
#             textcoords='offset points')

           
 
    def generateSequencesToFile(self, numberOfSequences):
        """this function generates sequences and inserts them into a file"""
        for i in range(1, numberOfSequences, 2):            
            with open('planning.txt', 'a') as f:
                f.write(str(i)+","+"\"alex\""+","+str(i)+","+str(i+2)+",2,12,-1\n")
    
    


    
    

           
    
        

        






        