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
        """
        


# tPrefereds =   (
#                     ('BEST_ELEVATION', '0'),                   
#                     ('IMMEDIATE', '1'),
#                     ('BETWEEN_JD1_JD2', '2'),  
#                     ('FIXED', 3),  
#                 )

import matplotlib.pyplot as plt

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
#         self.planStart = [planStart] 
#         self.planEnd = [planEnd]
#         self.durations = [planStart - planEnd ]
        
    def initFromMemory(self, sequences, planStart, planEnd): 
        self.mode = "CLASSIC"
        self.sequences = sequences
        self.intervals = [Interval(planStart, planEnd, planEnd-planStart) ,]
#         self.planStart = planStart
#         self.planEnd = planEnd
        self.currentSequence = sequences[0]
        self.currentTime = 1
        
    def initFromFile(self, fileName): 
        self.loadPlanningFromFile(fileName)  
        
                
                
                   
    def schedule(self):    
        if self.mode == "CLASSIC":
                        
            """pre-configuration : initial sorting by priority and jd2Owner"""
            
            self.initialSort()
                                        
            """loop through sequences which are TOBEPLANNED"""
            for seq in [i for i in self.sequences if i.status == "TOBEPLANNED"]:      
                
                """and try to plan them"""
                seq.status = "PLANNED" if self.placeSequence(seq) else "UNPLANABLE"
                 
                             
    def placeSequence(self, seq):
        
        """get indexes list of intervals where the interval duration is > duration of the sequence"""        
        longEnoughIntervals = self.filterByDuration(seq)
               
        if (longEnoughIntervals):  
             
            """if there are slots available"""                          
            return self.placeSequenceWithoutShift(longEnoughIntervals, seq)
         
        else:
             
            """no slots available, shift to make room"""
            return self.placeSequenceWithShift(seq)
                    
        

    def placeSequenceWithoutShift(self, longEnoughIntervals, seq):
        """place the sequence in the planning without relocating other sequences"""
       
        """
        for the list of intervals which have a duration greater than that of the sequence, choose just the ones that are between
        jd1Owner and jd2Owner
        """
        
        compatibleIntervals = [interval for interval in longEnoughIntervals if seq.tPrefered >= interval.start and seq.tPrefered <= interval.end]        
        
        intervalToBeUsed = compatibleIntervals[0] if compatibleIntervals else longEnoughIntervals[0] 
        Dj = intervalToBeUsed.start
        Fj = intervalToBeUsed.end
                   
        if seq.tPrefered == -1:   
            """this is the case where the user requests immediate observation, meaning tPrefered = -1 """   
                           
            seq.TSP = max(intervalToBeUsed.start, seq.jd1Owner)
            seq.TEP = seq.TSP + seq.duration
        else:
            """
                in case of choosing best elevation or between jd1Owner and jd2Owner for the tPrefered, the TSP and
                the TEP will be computed by subtracting and adding the duration accordingly
                TSP will be the tPrefered minus half the duration and TEP will be tPrefered plus the other half of the
                duration
            """
                       
            if compatibleIntervals:       
                                                               
                seq.TSP = seq.tPrefered-(seq.duration/2)
                seq.TEP = seq.tPrefered+(seq.duration/2)
                
                """adjusting TSP and TEP """
                
                if seq.TSP <= max(Dj, seq.jd1Owner):
                    seq.TSP = max(Dj, seq.jd1Owner)
                    seq.TEP = seq.TSP + seq.duration                    
                else:
                    if seq.TEP >= min(Fj, seq.jd2Owner):
                        seq.TEP = min(Fj, seq.jd2Owner)
                        seq.TSP = seq.TEP - seq.duration
                       
            else:
                
                if compatibleIntervals is None:
                
                    for interval in longEnoughIntervals:
                        if interval.start > seq.tPrefered:
                            seq.TSP = Dj                            
                            seq.TEP= seq.TSP + seq.duration
                        else:
                            if interval.end < seq.tPrefered:
                                self.TEP = Fj
                                self.TSP= self.TEP - self.duration     
                        break      
                       
        """compute the possiblity of shifting the sequences to make room for future sequences"""
        self.computeDeltaTL(Dj, seq)
        self.computeDeltaTR(Fj, seq)
        self.updateIntervals(intervalToBeUsed, seq)
        
        if seq.TSP == -1 or seq.TEP == -1:
            return False
        else:          
            return True
        
    def placeSequenceWithShift(self, seq):    
        """place the sequence in the largest available interval by shifting previous and/or next sequences"""
        print "Placement with shift"
        seq.display()
        """Look for the largest available interval between jd1Owner and jd2Owner. """
        possibleIntervals = []
        for interval in self.intervals:
            if interval.start >= seq.jd1Owner and interval.end <= seq.jd2Owner:
                possibleIntervals.append(interval)
        if len(possibleIntervals) == 0:
            """Abandon sequence, there are no available slots left"""            
            return False
        else:            
            """get the largest available interval between jd1Owner and jd2Owner"""
            import operator
            largestDurationInterval = max(self.intervals, key=operator.attrgetter('duration'))
                        
        """Test shift left: search for the sequence which ends at the start of the interval"""        
        resultLeftSequences = [sequence for sequence in self.sequences if sequence.TEP == largestDurationInterval.start]
        sequenceLeft = resultLeftSequences[0]
        print sequenceLeft.display()
        if sequenceLeft:
            """ check its shift left value """
            if sequenceLeft.deltaTL != 0 and sequenceLeft.sequencePriority >= seq.sequencePriority:            
                """TODO : Shift left sequence"""
                sequenceLeft.TSP -= sequenceLeft.deltaTL
                sequenceLeft.TEP = sequenceLeft.TSP + sequenceLeft.duration
                seq.TSP = sequenceLeft.TEP
                seq.TEP = seq.TSP + seq.duration
                self.updateIntervals(largestDurationInterval, sequenceLeft)
#                 self.updateIntervals(largestDurationInterval, seq)
                """Try to place the sequence, if it is not enough, check right shift"""
                
        else:
            """Try the right side"""
            """Test shift right: search for the sequence which starts in end of interval"""        
            sequenceRight = [i for i in self.sequences if i.TSP == largestDurationInterval.end]
            if sequenceRight:
                """ check its shift right value """
                if sequenceRight.deltaTR != 0 and sequenceRight.sequencePriority >= seq.sequencePriority:
                    """Try to place the sequence, if it is not enough, it is UNPLANNABLE"""
                    sequenceRight.TSP += sequenceRight.deltaTR
                    sequenceRight.TEP = sequenceRight.TSP + sequenceRight.duration
                    seq.TEP = sequenceRight.TSP
                    seq.TSP = seq.TEP  - seq.duration
                    
                    self.updateIntervals(largestDurationInterval, sequenceRight)
#                     self.updateIntervals(largestDurationInterval, seq)
                     
                else:
                    seq.status = "UNPLANABLE"
                         
        
                
        """Update shifts"""
        Dj = largestDurationInterval.start
        Fj = largestDurationInterval.end
        self.computeDeltaTL(Dj, seq)
        self.computeDeltaTR(Fj, seq)
        
        return True
       
               
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
        
        
   
    def getLargestcompatibleIntervals(self):
        """get largest interval where we can shift to place sequence"""        
        return max(self.intervals.duration)
    
    def computeDeltaTL(self, Dj, seq):
        """compute the possible value of shifting the sequence to the left"""
        seq.deltaTL = seq.TSP - max(Dj, seq.jd1Owner) if seq.tPrefered != -1 else 0     
     
    def computeDeltaTR(self, Fj, seq):
        """compute the possible value of shifting the sequence to the right"""
        seq.deltaTR = min(Fj, seq.jd2Owner) - seq.TEP if seq.tPrefered != -1 else 0
    
                    
    def display(self):       
          
        for interval in self.intervals:
            interval.display()
            
        for seq in self.sequences:            
            seq.display()

            
    def displayGUI(self):
        from matplotlib.ticker import FormatStrFormatter  
            
        if self.sequences is not None:      
            yAxisMin = -0.5
            yAxisMax = len(self.sequences) + 1
            xAxisMin = -1.5
            xAxisMax = self.intervals[len(self.intervals)-1].end
    
            plt.figure(figsize=(20,10))
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f')) 
            plt.yticks([a for a in range(0, len(self.sequences))]) 
            plt.xticks([a for a in range(0, self.intervals[len(self.intervals)-1].end+1)])            
#             plt.xticks(range(self.planStart[0], self.planEnd[len(self.planEnd)-1], JULIAN_SECOND*120), rotation='vertical')
            plt.grid(True)
            plt.xlabel('Sequences in planing')
            plt.ylabel('Evolution in time') 
            plt.title('Scheduling of sequences in time')
            plt.ylim([yAxisMin,yAxisMax])
            plt.xlim([xAxisMin, xAxisMax])     
            
            
            for a in range(0, len(self.sequences)):    
                plt.axhline(y=a, xmin=0, xmax=xAxisMax, hold=None, label='free')  
            
            y = 0             
            for seq in self.sequences:      
                self.plotSequence(seq, y)
                if (y>0):
                    a = 0
                    while a <= y:                    
                        self.plotSequence(self.sequences[a], y)
                        a += 1
                y+=1
            
    #         plt.legend()
            plt.show()
        else:
            print "No data available in planning"
        
    def plotSequence(self, seq, y):      
        
        plt.plot([seq.TSP, seq.TEP], [y, y], color='r', linestyle='-', linewidth=2, label='Seq'+str(seq.id)+'['+str(seq.TSP)+']['+str(seq.TEP)+']')            
        plt.plot(seq.TSP, y, marker='x', color='r', linewidth=3)
        plt.plot(seq.TEP, y, marker='x', color='r', linewidth=3)
        plt.plot(seq.tPrefered, y, marker='o', color='g', linewidth=3)
        plt.annotate('id_seq:'+str(seq.id), xy=((seq.TSP+seq.TEP)/2,y), xytext=(0, 20), ha='center',
            textcoords='offset points')
        plt.annotate('TSP', xy=(seq.TSP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
        plt.annotate('TEP', xy=(seq.TEP,y), xytext=(-5, 5), ha='center',
            textcoords='offset points')
        plt.annotate('TPref', xy=(seq.tPrefered,y), xytext=(0, -20), ha='center',
            textcoords='offset points')

    def getSequencesFromDB(self):
        """connect to db and get sequences """
        
    def loadPlanningFromFile(self, fileName):
        with open(fileName, 'r') as f:
#             print "Reading data in file "
            data = f.readlines()
            """remove comments"""
            parsedData1 = [i for i in data if i[0] != '#']
            """remove empty slots like \n"""
            parsedData2 = [i for i in parsedData1 if i != '\n']
            """instantiate objects"""
            mode = str(parsedData2[0].split('=')[1]).rstrip()
            planStart = []
            planStart.append(int(parsedData2[1].split('=')[1]))
            planEnd = []
            planEnd.append(int(parsedData2[2].split('=')[1]))
            sequences = []
            for i in range(3,len(parsedData2)):
                sequenceParameters = parsedData2[i].split(',')
                idSeq = sequenceParameters[0]
                """The owner data will be modified accordingly"""
                ownerName = sequenceParameters[1]
                owner = Owner(ownerName, 'France', 60)
                quota = Quota(owner, 100, 50,  60)
                jd1Owner = int(sequenceParameters[2])
                jd2Owner = int(sequenceParameters[3])
                duration = int(sequenceParameters[4])
                priority = int(sequenceParameters[5])
                tPreferedTime = int(sequenceParameters[6])
                seq = Sequence(idSeq, owner, jd1Owner, jd2Owner, duration, priority, tPreferedTime)
                sequences.append(seq)
#             print "Creating planning"  
            self.mode = mode
            self.planStart = planStart
            self.planEnd =  planEnd
            self.intervals = [].append(Interval(planStart[0], planEnd[0], planEnd[0]-planStart[0])) 
            self.currentSequence = sequences[0]
            self.currentTime = 1
            self.sequences = sequences  
#             print "Done"   
        f.closed
        
        






        