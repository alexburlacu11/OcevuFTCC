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
                   
                   
    tPref closest to jd1Owner, jd2Owner in case its outside visible interval
    
    jd - 20450404 et entre parantheses la date
    
    
                 
        """


import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter 
import operator
import copy

JULIAN_SECOND = 115740

class Sequence:
    def __init__(self, ident, owner, jd1Owner, jd2Owner, duration, sequencePriority, tPrefered):
        self.id = ident
        self.owner = owner
        self.jd1Owner = jd1Owner
        self.jd2Owner = jd2Owner        
        self.sequencePriority = sequencePriority
        self.duration = duration
        self.tPrefered = tPrefered   #temps en seconds compris entre jd1Owner et jd2Owner      
        self.status = "TOBEPLANNED"
        self.TSP = -1
        self.TEP = -1
        self.deltaTL = -1 
        self.deltaTR = -1
        
    def display(self):
        print "Seq:"+str(self.id)+" TSP:"+str(self.TSP)+" TEP:"+str(self.TEP)+" shiftLeft:"+str(self.deltaTL)+" shiftRight:"+str(self.deltaTR)+" priority:"+str(self.sequencePriority)+" status:"+str(self.status)
          
               
class Owner:
    def __init__(self, name, affiliation, priority):      
        self.name = name
        self.affiliation = affiliation
        self.priority = priority
        
        
class Quota:
    def __init__(self, owner, quota, quotaPartner, quotaRemaining):
        self.owner = owner
        self.quota = quota
        self.quotaPartner = quotaPartner
        self.quotaRemaining = quotaRemaining
        
    def addQuota(self, val ):
        self.quota += val
        
    def substractQuota(self, val):
        self.quota -= val
        
        
class Interval:
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration
   
    def display(self):
        print "["+str(self.start)+" - "+str(self.end)+"]"     
        
                
class Planning:
    def __init__(self, mode, sequences, currentSequence, currentTime, planStart, planEnd, ):
        """mode 1 classic entre 2 journees de planification, 2 cas alerte, 3 request, 4 apres alarme""" 
        self.mode = mode
        self.sequences = sequences
        self.currentSequence = currentSequence
        self.currentTime = currentTime               
        self.intervals = [Interval(planStart, planEnd, planEnd-planStart),]
        self.sequencesHistory = {}
        
    def initFromMemory(self, sequences, planStart, planEnd): 
        self.mode = "DEBUG"
        self.sequences = sequences
        self.intervals = [Interval(planStart, planEnd, planEnd-planStart) ,]
        self.currentSequence = sequences[0]
        self.currentTime = 1
        
    def initFromFile(self, fileName): 
        with open(fileName, 'r') as f:
#             print "Reading data in file "
            data = f.readlines()
            """remove comments"""
            parsedData1 = [i for i in data if i[0] != '#']
            """remove empty slots like \n"""
            parsedData2 = [i for i in parsedData1 if i != '\n']
            """instantiate objects"""
            mode = str(parsedData2[0].split('=')[1]).rstrip()
            planStart = float(parsedData2[1].split('=')[1])
            planEnd = float(parsedData2[2].split('=')[1]) 
            sequences = []
            for i in xrange(3,len(parsedData2)):
                sequenceParameters = parsedData2[i].split(',')
                idSeq = sequenceParameters[0]
                """The owner data will be modified accordingly"""
                ownerName = sequenceParameters[1]
                owner = Owner(ownerName, 'France', 60)
                quota = Quota(owner, 100, 50,  60)
                jd1Owner = float(sequenceParameters[2])
                jd2Owner = float(sequenceParameters[3])
                duration = (float(sequenceParameters[4])/86400.0)*100000000
                priority = float(sequenceParameters[5])
                tPreferedTime = float(sequenceParameters[6])
                seq = Sequence(idSeq, owner, jd1Owner, jd2Owner, duration, priority, tPreferedTime)
                sequences.append(seq)
#             print "Creating planning"             
            self.initFromMemory(sequences, planStart, planEnd)
#             print "Done"   
        f.closed               
                   
    def schedule(self):    
                                
        """pre-configuration : initial sorting by priority and jd2Owner"""          
        self.initialSort()
                                    
        """loop through sequences which are TOBEPLANNED"""
        instant = 0
        for seq in [sequence for sequence in self.sequences if sequence.status == "TOBEPLANNED"]:      
            
            """and try to plan them"""
            seq.status = "PLANNED" if self.placeSequence(seq) else "UNPLANABLE"
                           
            """save a history of the sequences and their states during the planning"""            
            if self.mode == "DEBUG":   
                self.saveInHistory(instant)
                instant += 1
            
                           
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
                   
        if seq.tPrefered == -1:   
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
        sequenceLeft = resultLeftSequences[0]
        if sequenceLeft.deltaTL != 0 and seq.duration <= sequenceLeft.deltaTL + longestInterval.duration:            
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
            sequenceRight = resultRightSequences[0]
            if sequenceRight.deltaTR != 0 and seq.duration <= sequenceRight.deltaTR + longestInterval.duration:
                """Try to place the sequence, if it is not enough, it is UNPLANNABLE"""
                self.insertSequence("LEFT", sequenceRight.TSP + sequenceRight.deltaTR, sequenceRight)
#                 self.updateIntervals(largestDurationInterval, sequenceRight)
                self.insertSequence("RIGHT", sequenceRight.TSP, seq)               
                self.updateIntervals(longestInterval, seq)             
            else:
                """Try to shift to the left first then to the right"""
                if seq.duration <= sequenceRight.deltaTR + sequenceLeft.deltaTL + longestInterval.duration and \
                    sequenceLeft.deltaTL != 0 and sequenceRight.deltaTR != 0:
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
        self.sequences.sort(key=lambda x: ( x.sequencePriority, x.jd2Owner ), reverse=False)
        
    def filterByDuration(self, seq):
        """ Search for an interval where the duration is > duration of the sequence"""
        longEnoughIntervals = []
        for interval in self.intervals:
            leftLimit = max(interval.start,seq.jd1Owner)
            rightLimit = min(interval.end,seq.jd2Owner)
            if rightLimit - leftLimit >= seq.duration:
                longEnoughIntervals.append(interval)
        return longEnoughIntervals

           
    def updateIntervals(self, usedInterval, seq):
        """update new free intervals"""
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

            
    def displayGUI(self):
                     
        if self.sequences is not None:      
            yAxisMin = -0.5
            yAxisMax = len(self.sequences) + 1
            xAxisMin = -1.5
            xAxisMax = self.intervals[len(self.intervals)-1].end + 1
    
            plt.figure(figsize=(20,10), facecolor='orange')
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f')) 
            plt.yticks([a for a in xrange(0, len(self.sequences))]) 
#             plt.xticks([a for a in xrange(0.0, self.intervals[len(self.intervals)-1].end+1)])            
#             plt.xticks(xxrange(self.planStart[0], self.planEnd[len(self.planEnd)-1], JULIAN_SECOND*120), rotation='vertical')
            plt.grid(True)
            plt.xlabel('Sequences in planing')
            plt.ylabel('Evolution in time') 
            plt.title('Example featuring the rescheduling of 2 sequences to make room for the third')
            plt.ylim([yAxisMin,yAxisMax])
            plt.xlim([xAxisMin, xAxisMax])     
            
            for a in xrange(0, len(self.sequences)):    
                plt.axhline(y=a, xmin=0, xmax=xAxisMax, hold=None, label='free')  
            
            for i in xrange(0, len(self.sequences)):
                ss = self.sequencesHistory[i]    
                   
                for seq in ss:
                    self.plotSequence(seq, i)
            
    #         plt.legend()
            plt.show()
        else:
            print "No data available in planning"
        
    def plotSequence(self, seq, y):      
        
        plt.plot([seq.TSP, seq.TEP], [y, y], color='r', linestyle='-', linewidth=5, label='Seq'+str(seq.id)+'['+str(seq.TSP)+']['+str(seq.TEP)+']')            
        plt.plot(seq.TSP, y, marker='o', color='g', linewidth=8)
        plt.plot(seq.TEP, y, marker='o', color='g', linewidth=8)
        plt.plot(seq.tPrefered, y, marker='p', color='m', linewidth=8)
        plt.annotate('seq: '+str(seq.id), xy=((seq.TSP+seq.TEP)/2,y), xytext=(0, 20), ha='center',
            textcoords='offset points')
        plt.annotate('TSP', xy=(seq.TSP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
        plt.annotate('TEP', xy=(seq.TEP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
        plt.annotate('TPref', xy=(seq.tPrefered,y), xytext=(0, -20), ha='center',
            textcoords='offset points')

           
 
    def generateSequencesToFile(self, numberOfSequences):
        """this function generates sequences and inserts them into a file"""
        for i in range(1, numberOfSequences, 2):            
            with open('planning.txt', 'a') as f:
                f.write(str(i)+","+"\"alex\""+","+str(i)+","+str(i+2)+",2,12,-1\n")

        
        






        