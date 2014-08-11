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
        
        
class Planning:
    def __init__(self, mode, sequences, currentSequence, currentTime, planStart, planEnd, ):
        """mode 1 classic entre 2 journees de planification, 2 cas alerte, 3 request, 4 apres alarme"""
        self.mode = mode
        self.sequences = sequences
        self.currentSequence = currentSequence
        self.currentTime = currentTime               
        self.planStart = [planStart]
        self.planEnd = [planEnd]
        self.durations = [planStart - planEnd ]
        
#     def schedule(self):
#         
#         if self.mode == "CLASSIC":
#             print "classic"
#             """pre-configuration"""
#             self.updateDurations()
#                                   
#             self.initialSort()
#                                        
#             """loop through sequences"""
#             for seq in self.sequences:
#             
#                 
#                 #self.computetPreferedTime(seq)
#                 
#                 print seq.tPrefered
#                 
#                 indexesFromDuration = self.filterByDuration(seq)
#                 
#                 if (indexesFromDuration is not None):  
#                     
#                     """if there are slots available"""
#                          
#                     indexesFromJDs = self.filterByInterval(seq, indexesFromDuration)
#                     
#                     if seq.tPrefered == -1:
#                         
#                         placementIndex = indexesFromDuration[0]
#                         
#                         self.placeSequence(-1, placementIndex, seq)
#                         
#                     else:
#                         
#                         """YES there are slots available"""
#                         
#                         result = self.filterBytPrefered(seq, indexesFromJDs)                     
#                         print seq.tPrefered
#                         placementIndex = result[0]           
#                         
#                         self.placeSequence("OTHER", placementIndex, seq)
#                 
#                 else:
#                     
#                     """no slots available, shift to make room"""
#                     
#                     largestIntervalIndex = self.getLargestIntervalIndex()
#                     
#                     print "Index of largest interval: "+ str(largestIntervalIndex)
#                     
#                     """
#                         get sequence before and after
#                         compute shift left for before sequence
#                         compute shift right for after sequence
#                         shift them
#                         place sequence
#                     """
#                     Dj = self.planStart[largestIntervalIndex]
#                     Fj = self.planEnd[largestIntervalIndex]
# #                     deltaTR = deltaTL = 0
# #                     if seq.option == "IMMEDIATE" or seq.option == "FIXED":
# #                         deltaTR = deltaTL = 0
# #                     else:
# #                         
# #                         deltaTL = self.getLeftShift(Dj, previousSequence)
# #                         deltaTR = self.getRightShift(Fj, nextSequence)
#                     
#                             
#                 self.updateDurations()
#                 
#             else:
#                 if self.mode == "ALERT":
#                     """do stuff"""
                
                
                   
    def schedule(self):    
        if self.mode == "CLASSIC":
            
            print "classic"
            
            """pre-configuration"""
            
            """update interval durations"""
            self.updateDurations()
            
            """sort sequences by priority and jd2Owner"""                       
            self.initialSort()
                                        
            """loop through sequences"""
            for seq in self.sequences:
                
                """Get indexes list of intervals where the interval duration is > duration of the sequence""" 
                indexFromDuration = self.filterByDuration(seq)
                                
                if (indexFromDuration):  
                    """if there are slots available"""
                    self.placeSequence("DIRECT", indexFromDuration, seq)
                                     
                else:                                        
                    """no slots available, shift to make room"""
                    self.placeSequence("DELAY", indexFromDuration, seq)
                     

    def placeSequence(self, option, indexes, seq):
        
        intervalIndex = [i for i in indexes if seq.tPrefered >= self.planStart[i] and seq.tPrefered <= self.planEnd[i]]
        print indexes         
        if option == "DIRECT":
            """put the sequence in the right place"""
            
            if seq.tPrefered == -1:                
                seq.TSP = max(self.planStart[indexes[0]], seq.jd1Owner)
                seq.TEP = seq.TSP + seq.duration
                self.planEnd.append(self.planEnd[indexes[0]])
                self.planEnd[indexes[0]] = seq.TSP
                self.planStart.append(seq.TEP)
            else:
                Dj = self.planStart[intervalIndex[0]]
                Fj = self.planEnd[intervalIndex[0]]
                if seq.tPrefered != -1 and intervalIndex is not None:       
                    print "bla"
                    seq.TSP = max(Dj, max(seq.jd1Owner, seq.tPrefered-(1/2)*(seq.duration)))
                    seq.TEP = min(Fj, min(seq.jd2Owner, seq.tPrefered-(1/2)*(seq.duration)))
                    print seq.TSP 
                    print seq.TEP
                    if seq.TSP < max(Dj, seq.jd1Owner):
                        seq.TSP = max(Dj, seq.jd1Owner)
                        seq.TEP = seq.TSP + seq.duration
                        print "bla1"
                    else:
                        if seq.TEP > min(Fj, seq.jd2Owner):
                            seq.TEP = min(Fj, seq.jd2Owner)
                            seq.TSP = seq.TEP - seq.duration
                            print "bla2"
                else:
                    if seq.tPrefered != -1 and intervalIndex is None:
                        for i in indexes:
                            if self.planStart[i] > seq.tPrefered:
                                seq.TSP = Dj
                                
                                seq.TEP= seq.TSP + seq.duration
                            else:
                                if self.planEnd[i] < seq.tPrefered:
                                    self.TEP = Fj
                                    self.TSP= self.TEP - self.duration     
                            break      
                self.planEnd.append(Fj)
                self.planEnd[intervalIndex[0]] = seq.TSP
                self.planStart.append(seq.TEP)   
        else:
            if option == "DELAY":
                """make room for the sequence"""
                
        seq.status = "PLANNED"
        self.updateDurations()
        
        
#     def placeSequence(self, option, index, seq):
#        
#         Dj = self.planStart[index]
#         Fj = self.planEnd[index]
#         
#         
#         if (seq.tPrefered == -1): #if we don't have a tPrefered time but its not immediate
#             TRef1 = Dj
#             TRef2 = TRef1 + seq.duration
#         else:#case of best eleve or middle between jd1Owner and jd2Owner
#             TRef1 = seq.tPrefered - seq.duration/2
#             TRef2 = seq.tPrefered + seq.duration/2
#                 
#                       
#         if TRef1 < Dj or TRef2 > Fj:
#             """if TRef1 and TRef2 are NOT included in Dj and Fj""" 
#             if TRef1 < Dj:
#                 seq.TSP = Dj
#                 seq.TEP = Dj + seq.duration
#                 seq.status = "PLANNED"
#                 Dj = Dj + seq.duration                
#             if TRef2 > Fj:
#                 seq.TSP = Fj - seq.duration
#                 seq.TEP = Fj
#                 seq.status = "PLANNED"
#                 Fj = Fj - seq.duration
#         else:            
#             """if TRef1 and TRef2 are included in Dj and Fj"""
#             print "IMMEDIATE case else"
#             seq.TSP = TRef1
#             seq.TEP = TRef2
#             seq.status = "PLANNED"                
#             self.planEnd.append(Fj)
#             self.planEnd[index] = TRef1
#             self.planStart.append(TRef2)
# #                 self.planStart[index+2] = self.planStart[index+1]
       
        
            
    def initialSort(self):
        """sort ascending according to priority and jd2Owner"""
        """TODO: sort by tPrefered instead of jd2 ?? to gain in precision????????"""
        self.sequences.sort(key=lambda x: ( x.sequencePriority, x.jd2Owner ), reverse=False)
        
    def filterByDuration(self, seq):
        """ 1. Search for an interval where the duration is > duration of the sequence"""
        indexesFromDuration = []
        for i, duration in enumerate(self.durations):
            leftLimit = max(self.planStart[i],seq.jd1Owner)
            rightLimit = min(self.planEnd[i],seq.jd2Owner)
            if rightLimit - leftLimit >= seq.duration:
                indexesFromDuration.append(i)
                break
        return indexesFromDuration
#             print "indexes from durations: "+str(indexesFromDuration)

    def filterByInterval(self, seq, indexes ):
        """ 2-3. Search for an index where jd1Owner and jd2Owner are between start and end"""
        indexesFromJDs = []
        for i in indexes:
            Dj = self.planStart[i]
            Fj = self.planEnd[i]
            if Dj <= seq.jd1Owner and Fj - seq.jd1Owner >= seq.duration:
                indexesFromJDs.append(i)
            else: 
                if Fj >= seq.jd2Owner and seq.jd2Owner - Dj >= seq.duration:
                    indexesFromJDs.append(i)
        return indexesFromJDs
#             print "indexes from jd: "+str(indexesFromJDs)

    def filterBytPrefered(self, seq, indexes):
        """ 4. Search for an index where tPrefered time is between Dj and Fj"""
        result = []
        for i in indexes:
            Dj = self.planStart[i]
            Fj = self.planEnd[i]   
#                 print "i = "+str(i)             
            if seq.tPrefered >= Dj and seq.tPrefered <= Fj:
                result.append(i)                
                break;
        return result
          
    def updateDurations(self):
        self.planStart.sort()
        self.planEnd.sort()
        """for each pair start-end update duration"""
        self.durations = [i - j for i, j in zip(self.planEnd, self.planStart)]
            
    def updateIntervals(self, index, jd1, jd2):
        """update new free intervals"""
        print "updating intervals: "
        print self.planStart
        print self.planEnd
        oldEnd = self.planEnd[len(self.planEnd)-1]
        self.planEnd[index] = jd1
        self.planStart.append(jd2)
        self.planEnd.append(oldEnd)
        print "done: "
        print self.planStart
        print self.planEnd
   
    def getLargestIntervalIndex(self):
        """get largest interval where we can shift to place sequence"""        
        return self.durations.index(max(self.durations))
    
    def computeDeltaTL(self, Dj, previousSequence):
        """compute the possible value of shifting the sequence to the left"""
        deltaTL = previousSequence.TSP - max([Dj, previousSequence.jd1Owner])
        return deltaTL        
     
    def computeDeltaTR(self, Fj, nextSequence):
        """compute the possible value of shifting the sequence to the right"""
        deltaTR = min([Fj, nextSequence.jd2Owner]) - nextSequence.TEP
        return deltaTR
    
    def computetPreferedTime(self, seq):
        if seq.option == "IMMEDIATE":
            seq.tPrefered = -1
        else:
            if seq.option == "BEST_ELEVATION":
                seq.tPrefered = (seq.jd1Owner + seq.jd2Owner) / 2 #change it to ext ./astro program
            else:
                if seq.option == "BETWEEN_JD1_JD2":
                    seq.tPrefered = (seq.jd1Owner + seq.jd2Owner) / 2
                else:
                    seq.tPrefered = -1
            
        
                    
            
    def display(self):       
        print self.planStart
        print self.planEnd  
        count = 1
        for i in self.sequences:            
            print "Seq:"+str(i.id)+" TSP:"+str(i.TSP)+" TEP:"+str(i.TEP)+" priority:"+str(i.sequencePriority)+" status:"+str(i.status)
            count += 1 
            
    def displayGUI(self):
        from matplotlib.ticker import FormatStrFormatter  
    
             
        if self.sequences is not None:      
            yAxisMin = -0.5
            yAxisMax = len(self.sequences) + 1
            xAxisMin = -1.5
            xAxisMax = self.planEnd[len(self.planEnd)-1]+1
    
            plt.figure(figsize=(20,10))
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f')) 
            plt.yticks([a for a in range(0, len(self.sequences))]) 
            plt.xticks([a for a in range(0, self.planEnd[len(self.planEnd)-1]+1)])            
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
        
    def loadPlanningFromFile(self):
        with open('planning.txt', 'r') as f:
            print "Reading data in file "
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
            print "Creating planning"  
            self.mode = mode
            self.planStart = planStart
            self.planEnd =  planEnd
            self.currentSequence = sequences[0]
            self.currentTime = 1
            self.sequences = sequences  
            print "Done"   
        f.closed
        
        

class Tests:


    intervals = []
    sequences = []
    
    
    owner1 = Owner("John", 'France', 60)
    quota1 = Quota(owner1, 100, 50,  60)
    owner2 = Owner("Mike", 'France', 50)
    quota2 = Quota(owner2, 100, 50, 60)
    owner3 = Owner("Alan", 'Mexico', 40)
    quota3 = Quota(owner3, 100, 50, 60)
    
#     s1 = Sequence(1, owner1, 2, 5, 3, 4, 12, 2, 4, "TOBEPLANNED")
#     s2 = Sequence(2, owner1, 7, 10, 7, 10, 11, 2, 7, "TOBEPLANNED")
#     s3 = Sequence(3, owner1, 13, 17, 14, 17, 13, 2, 14, "TOBEPLANNED")
#     s4 = Sequence(4, owner1, 2, 4, 11, 2, 2)
#     s5 = Sequence(5, owner2, 2, 5, 11, 2, 5)
#     s6 = Sequence(6, owner3, 2, 4, 11, 2, 3)
#     s7 = Sequence(7, owner3, 2, 4, 11, 2, 8)


    def test1a(self):
        """test 1a: insert one sequence and test insertion according to duration"""
        print '---Test 1a: duration for one sequence'
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, 4)
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display()
    
    def test1b(self):
        """test 1b: duration for two sequences"""
        print '---Test 1b: duration for two sequences'
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, 4)
        s2 = Sequence(2, self.owner1, 7, 10, 2, 11, 8)
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1, s2]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display()
        
    def test1c(self):
        """test 1c: immediate sequence scheduling, plan start = TSP"""
        print '---Test 1c: immediate sequence scheduling, plan start = TSP'
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)  
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1]
        planStart = 3
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display() 
        
    def test1d(self):
        """test 1d: immediate sequence scheduling - choose first available slot which contains duration"""
        print '---Test 1d: immediate sequence scheduling'
        print ' - choose first available slot which contains duration'
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)        
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1]
        planStart = 4
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display()   

    def test2a(self):
        """test 2a: TRef undetermined jd1Owner and jd2Owner known"""
        print '---Test 2a: TRef undetermined jd1Owner and jd2Owner known'        
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)        
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display()   
        
    def test2b(self):
        """test 2b: TRef undetermined jd1Owner and jd2Owner known with 2 sequences"""
        print '---Test 2a: TRef undetermined jd1Owner and jd2Owner known with 2 sequences'        
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)        
        s2 = Sequence(2, self.owner1, 3, 5, 2, 12, -1)     
        s3 = Sequence(3, self.owner1, 3, 5, 2, 12, -1)      
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1,s2,s3]
        planStart = 3
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        print '-------Before------'
        plan.display()
        print '-------Scheduling------'
        plan.schedule()
        print '-------After-------'
        plan.display()  
    
        
    def testPlanPlot(self):
        """test Plot: Plot sequences and intervals"""
        print '---Test Plot: Plot sequences and intervals'        
        s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)   
        s2 = Sequence(2, self.owner1, 7, 10, 3, 12, -1)    
        s3 = Sequence(3, self.owner1, 15, 18, 3, 12, 15) 
        s4 = Sequence(4, self.owner1, 17, 19, 2, 12, 17)
        s5 = Sequence(5, self.owner1, 5, 8, 3, 12, 6)
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1, s2, s3, s4, s5]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        plan.schedule()
        plan.displayGUI()
        
    def testLoadFromFile(self):
        """test File: Load planning from file"""
        print '---Test Files: Load planning from file'        
        plan = Planning( 0, None, 0, 0, 0, 0)
        print '-------Before------'
        plan.loadPlanningFromFile()
        plan.display()
        print '-------Scheduling------'        
        plan.schedule()
        print '-------After-------'
        plan.display()
        plan.displayGUI() 
        

def main():
    print "--------------Starting tests--------------"
    testSuite = Tests()
    testSuite.test1a()   
#     testSuite.test1b()    
#     testSuite.test1c()
#     testSuite.test1d()
#     testSuite.test2a()
#     testSuite.test2b()
    testSuite.testPlanPlot()
    testSuite.testLoadFromFile()

if __name__ == '__main__':
    main()





        