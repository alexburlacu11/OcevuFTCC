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
        


# preferences =   (
#                     ('BEST_ELEVATION', '0'),                   
#                     ('IMMEDIATE', '1'),
#                     ('BETWEEN_JD1_JD2', '2'),  
#                     ('FIXED', 3),  
#                 )

class Sequence:
    def __init__(self, ident, owner, jd1, jd2, jd1Owner, jd2Owner, sequencePriority, duration, preference, option):
        self.id = ident
        self.owner = owner
        self.jd1 = jd1
        self.jd2 = jd2
        self.jd1Owner = jd1Owner
        self.jd2Owner = jd2Owner        
        self.sequencePriority = sequencePriority
        self.duration = duration
        self.preference = preference   #temps en seconds compris entre jd1 et jd2 
        self.option = option          
        self.status = "TOBEPLANNED"
        self.TDP = -1
        self.TFP = -1
        
               
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
        self.start = [planStart]
        self.end = [planEnd]
        self.durations = [planStart - planEnd ]
        
    def schedule(self):
        
        if self.mode == "CLASSIC":
            
            """pre-configuration"""
            self.updateDurations()
                                  
            self.initialSort()
                                       
            """loop through sequences"""
            for seq in self.sequences:
                
                """compute temps de preference, do not input it by hand"""
                
                indexesFromDuration = self.filterByDuration(seq)
                
                if (indexesFromDuration is not None):  
                    
                    """if there are slots available"""
                         
                    indexesFromJDs = self.filterByInterval(seq, indexesFromDuration)
                    
                    if seq.option == "IMMEDIATE":
                        
                        placementIndex = indexesFromDuration[0]
                        
                        self.placeSequence("IMMEDIATE", placementIndex, seq)
                        
                    else:
                        
                        result = self.filterByPreference(seq, indexesFromJDs)                     
                        
                        placementIndex = result[0]           
                        
                        self.placeSequence("OTHER", placementIndex, seq)
                
                else:
                    
                    """no slots available, shift to make room"""
                    
                    largestIntervalIndex = self.getLargestIntervalIndex()
                    
                    print "Index of largest interval: "+ str(largestIntervalIndex)
                    
                    """
                        get sequence before and after
                        compute shift left for before sequence
                        compute shift right for after sequence
                        shift them
                        place sequence
                    """
                    Dj = self.start[largestIntervalIndex]
                    Fj = self.end[largestIntervalIndex]
#                     TAID = TAIG = 0
#                     if seq.option == "IMMEDIATE" or seq.option == "FIXED":
#                         TAID = TAIG = 0
#                     else:
#                         
#                         TAIG = self.getLeftShift(Dj, previousSequence)
#                         TAID = self.getRightShift(Fj, nextSequence)
                    
                            
                self.updateDurations()
                
                
                   
        
    def placeSequence(self, option, index, seq):
       
        Dj = self.start[index]
        Fj = self.end[index]
        
        if (option == "IMMEDIATE"):
            print "IMMEDIATE case"
            TRef1 = seq.jd1Owner
            TRef2 = seq.jd2Owner               
        else:
            if (seq.preference == -1): #if we don't have a preference time but its not immediate
                TRef1 = Dj
                TRef2 = TRef1 + seq.duration
            else:#case of best eleve or middle between jd1Owner and jd2Owner
                TRef1 = seq.preference - seq.duration/2
                TRef2 = seq.preference + seq.duration/2
                
                      
        if TRef1 < Dj or TRef2 > Fj:
            """if TRef1 and TRef2 are NOT included in Dj and Fj""" 
            if TRef1 < Dj:
                seq.TDP = Dj
                seq.TFP = Dj + seq.duration
                seq.status = "PLANNED"
                Dj = Dj + seq.duration                
            if TRef2 > Fj:
                seq.TDP = Fj - seq.duration
                seq.TFP = Fj
                seq.status = "PLANNED"
                Fj = Fj - seq.duration
        else:            
            """if TRef1 and TRef2 are included in Dj and Fj"""
            print "IMMEDIATE case else"
            seq.TDP = TRef1
            seq.TFP = TRef2
            seq.status = "PLANNED"                
            self.end.append(Fj)
            self.end[index] = TRef1
            self.start.append(TRef2)
#                 self.start[index+2] = self.start[index+1]
       
        
            
    def initialSort(self):
        """sort according to priority and jd2"""
        """sort by temps de preferance instead of jd2 ?? to gain in precision"""
        self.sequences.sort(key=lambda x: ( x.sequencePriority, x.jd2 ), reverse=False)
        
    def filterByDuration(self, seq):
        """ 1. Search for an interval where the duration is > duration of the sequence"""
        indexesFromDuration = []
        for i, duration in enumerate(self.durations):
            if seq.duration <= duration:
                indexesFromDuration.append(i)
        return indexesFromDuration
#             print "indexes from durations: "+str(indexesFromDuration)

    def filterByInterval(self, seq, indexes ):
        """ 2-3. Search for an index where jd1Owner and jd2Owner are between start and end"""
        indexesFromJDs = []
        for i in indexes:
            Dj = self.start[i]
            Fj = self.end[i]
            if Dj <= seq.jd1Owner and Fj - seq.jd1Owner >= seq.duration:
                indexesFromJDs.append(i)
            else: 
                if Fj >= seq.jd2Owner and seq.jd2Owner - Dj >= seq.duration:
                    indexesFromJDs.append(i)
        return indexesFromJDs
#             print "indexes from jd: "+str(indexesFromJDs)

    def filterByPreference(self, seq, indexes):
        """ 4. Search for an index where preference time is between Dj and Fj"""
        result = []
        for i in indexes:
            Dj = self.start[i]
            Fj = self.end[i]   
#                 print "i = "+str(i)             
            if seq.preference >= Dj and seq.preference <= Fj:
                result.append(i)                
                break;
        return result
          
    def updateDurations(self):
        self.start.sort()
        self.end.sort()
        """for each pair start-end update duration"""
        self.durations = [i - j for i, j in zip(self.end, self.start)]
            
    def updateIntervals(self, index, jd1, jd2):
        """update new free intervals"""
        print "updating intervals: "
        print self.start
        print self.end
        oldEnd = self.end[len(self.end)-1]
        self.end[index] = jd1
        self.start.append(jd2)
        self.end.append(oldEnd)
        print "done: "
        print self.start
        print self.end
   
    def getLargestIntervalIndex(self):
        """get largest interval where we can shift to place sequence"""        
        return self.durations.index(max(self.durations))
    
    def getLeftShift(self, Dj, previousSequence):
        """compute the possible value of shifting the sequence to the left"""
        TAIG = previousSequence.TDP - max([Dj, previousSequence.jd1Owner])
        return TAIG
        
     
    def getRightShift(self, Fj, nextSequence):
        """compute the possible value of shifting the sequence to the right"""
        TAID = min([Fj, nextSequence.jd2Owner]) - nextSequence.TFP
        return TAID
            
    def display(self):       
        print self.start
        print self.end  
        count = 1
        for i in self.sequences:            
            print "Seq:"+str(i.id)+" TDP:"+str(i.TDP)+" TFP:"+str(i.TFP)+" priority:"+str(i.sequencePriority)+" status:"+str(i.status)
            count += 1 
            
    def displayPlot(self):
        import matplotlib.pyplot as plt
        plt.plot(self.start, self.end, 'ro')
        plt.plot(self.durations, 'ro')
        plt.show()

    def getSequencesFromDB(self):
        """connect to db and get sequences """
        
    def loadPlanningFromFile(self):
        with open('planning.txt', 'r') as f:
            read_data = f.read()
            print read_data            
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
        """test 1a: duration for one sequence"""
        print '---Test 1a: duration for one sequence'
        s1 = Sequence(1, self.owner1, 2, 5, 3, 4, 12, 2, 4, "BETWEEN_JD1_JD2")
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
        s1 = Sequence(1, self.owner1, 2, 5, 3, 4, 12, 2, 4, "BETWEEN_JD1_JD2")
        s2 = Sequence(2, self.owner1, 7, 10, 7, 10, 11, 2, 7, "BETWEEN_JD1_JD2")
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
        """test 1c: immediate sequence scheduling, plan start = TDP"""
        print '---Test 1c: immediate sequence scheduling, plan start = TDP'
        s1 = Sequence(1, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")  
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
        s1 = Sequence(1, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")        
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
        s1 = Sequence(1, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")        
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
        s1 = Sequence(1, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")        
        s2 = Sequence(2, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")     
        s3 = Sequence(3, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")      
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
        
    def testLoadFromFile(self):
        """test File: Load planning from file"""
        print '---Test Files: Load planning from file'        
        plan = Planning( 0, 0, 0, 0, 0, 0)
        plan.loadPlanningFromFile()
        
    def testPlanPlot(self):
        """test Plot: Plot sequences and intervals"""
        print '---Test Plot: Plot sequences and intervals'        
        s1 = Sequence(1, self.owner1, 2, 6, 3, 5, 12, 2, -1, "IMMEDIATE")        
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        plan.displayPlot()
        
        """
        add imediate test with other sequences in the plannification
        """

def main():
    print "--------------Starting tests--------------"
    testSuite = Tests()
    testSuite.test1a()   
    testSuite.test1b()    
    testSuite.test1c()
    testSuite.test1d()
    testSuite.test2a()
    testSuite.test2b()
    testSuite.testLoadFromFile()
    testSuite.testPlanPlot()

if __name__ == '__main__':
    main()





        