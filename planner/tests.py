from django.test import TestCase

import unittest
from planner.models import Planning, Owner, Sequence, Quota, SequenceOrder, Interval
import time as t
from decimal import * 


   

class Test_Suite_for_Planner(unittest.TestCase):
    
    """Note: priority remains the same after initial sorting tests"""

    def setUp(self):
        """"
        Set up the environment. Create a new empty planning and some sequences. 
        Use test sequences to insert in planningning according to the test objectives
        
        SET GLOBAL query_cache_size = 0;

        Read more : http://www.ehow.com/how_12186816_disable-query-mysql-cache.html


        """
        print("SETUP")
        try:
            if self.s1: print("S1 EXISTE !!!")
            else: print("s1 non existante")
        except:
            print("coucou")
        self.planning = Planning( 0.0, [] , 0.0, 0.0, 0.0, 0.0)
#         self.planStart = 2456959.18000000
#         self.planEnd =   2456959.99000000
        self.planStart = 1
        self.planEnd =   10
        self.owner1 = Owner(name="John", affiliation='France', priority=60)
        self.owner1.save()
        self.quota1 = Quota(owner=self.owner1, quotaNightTotal=100, quotaNightLeft=60)
        self.quota1.save()
        """simple database sequences for performance testing"""
        self.s1 = Sequence(id=1, owner=self.owner1, jd1Owner=3, jd2Owner=5, duration=2, priority=12, tPrefered=-1)
        self.s2 = Sequence(id=2, owner=self.owner1, jd1Owner=8, jd2Owner=12, duration=4, priority=12, tPrefered=9)        
        
        """delay tests"""
        """both left and right"""
        self.s17 = Sequence(id=17, owner=self.owner1, jd1Owner=1, jd2Owner=8, duration=6, priority=12, tPrefered=5)
        self.s18 = Sequence(id=18, owner=self.owner1, jd1Owner=14, jd2Owner=20, duration=4, priority=12, tPrefered=16)
        self.s1718 = Sequence(id=1718, owner=self.owner1, jd1Owner=1, jd2Owner=20, duration=9, priority=12, tPrefered=12 )
        
        """complex tests"""
        self.s20 = Sequence(id=20, owner=self.owner1, jd1Owner=1, jd2Owner=8, duration=6, priority=12, tPrefered=5)
        self.s21 = Sequence(id=21, owner=self.owner1, jd1Owner=3, jd2Owner=5, duration=2, priority=12, tPrefered=-1)
        self.s22 = Sequence(id=22, owner=self.owner1, jd1Owner=7, jd2Owner=12, duration=5, priority=12, tPrefered=-1)
        
    """Reusable tests and other functions"""   
    def subtest_PLAN_unit_planner_Planning_schedule_orderNSequences(self):
        """Check that all sequences are in the proper order"""
        
        numberOfSequences = len(self.planning.sequences)
        print("Nr of seq:" +str(numberOfSequences))
        for i in range(0, numberOfSequences-1):
            self.assertLessEqual(self.planning.sequences[i].TSP, self.planning.sequences[i+1].TSP)
            self.assertLessEqual(self.planning.sequences[i].TEP, self.planning.sequences[i+1].TEP)
            self.assertLessEqual(self.planning.sequences[i].TEP, self.planning.sequences[i+1].TSP)
            
    def subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift(self):
        """Checks that the sequence following a shift is correctly placed"""
        numberOfSequences = len(self.planning.sequences)
        print("Nr of seq:" +str(numberOfSequences))
        self.assertTrue(self.planning.sequences[2].TSP >= self.planning.sequences[0].TSP)
        self.assertTrue(self.planning.sequences[2].TEP >= self.planning.sequences[0].TEP)
        self.assertTrue(self.planning.sequences[2].TSP <= self.planning.sequences[1].TSP)
        self.assertTrue(self.planning.sequences[2].TEP <= self.planning.sequences[1].TEP)
        self.assertTrue(self.planning.sequences[2].TSP >= self.planning.sequences[0].TEP)
        self.assertTrue(self.planning.sequences[2].TEP <= self.planning.sequences[1].TEP)
    
    def avg(self, myList):
        """ computes the average of a list of integers """
        s = 0
        for elm in myList:
            s += elm            
        return str(s/(len(myList)*1.0))
        
                
        
    """CADOR sequences tests"""
    
#     def test_PLAN_planner_Planning_schedule_planSequencesFromCador(self):
#         """
#         precond: sequences in database, empty planning
#         action: Test if the planning is correctly loaded with the sequences from the db
#         postcond: non empty planning
#         """
#         self.planning.initFromCador(self.owner1, self.quota1)    
#         self.planning.initFromDB(self.planStart, self.planEnd)             
#         myList = []
#         f = open('workfile.txt', 'r+')
#         for i in xrange(0,1):           
#             t0 = t.clock()
#             self.planning.schedule()
#             t1 = t.clock()
# #             self.planning = Planning( 0.0, [] , 0.0, 0.0, 0.0, 0.0)
# #             Sequence.objects.all().delete() 
# #             SequenceOrder.objects.all().delete()
#             myList.append(t1-t0)           
#             f.write("Try: "+str(i)+" "+str(t0) + " " + str(t1) + " " + str(t1-t0) + "\n")      
#         f.write("\naverage: \n"+self.avg(myList))
#         f.write("\nmin: \n"+str(min(myList)))
#         f.write("\nmax: \n"+str(max(myList)))
#         f.close()      
#         self.planning.display()
#         #self.planning.displayGUI()    

 
#     def test_PLAN_planner_Planning_schedule_planningKlotz(self):
#         """
#         precond: sequences in database, empty planning
#         action: Test if the planning is correctly loaded with the sequences from the db
#         postcond: non empty planning
#         """
#         self.planning.initFromCador(self.owner1, self.quota1)    
#         self.planning.initFromDB(self.planStart, self.planEnd)
# #         self.planning.display()
#         self.planning.schedule()
#         self.planning.display()
#         listOfSeqInNewPlanning = self.planning.getPlanningSequenceIDs()
#         print( "Total seq in my planning:")
#         print( len(listOfSeqInNewPlanning) )
#         listOfSeqInKlotz= self.planning.getKlotzSequenceIDs()
#         print( "Total seq in Klotz planning:")
#         print( len(listOfSeqInKlotz)    )
#         
#         print( "Seq in Klotz that are not in my planning" )
#         print( list(set(listOfSeqInKlotz) - set(listOfSeqInNewPlanning)) )
#         print( len(list(set(listOfSeqInKlotz) - set(listOfSeqInNewPlanning))) )
#         print( "Seq in Planning that are not in Klotz planning")
#         print( list(set(listOfSeqInNewPlanning) - set(listOfSeqInKlotz)))
#         print( len(list(set(listOfSeqInNewPlanning) - set(listOfSeqInKlotz))))
#         print( "Seq in Planning that are both in my planning and in Klotz")
#         print( list(set(listOfSeqInNewPlanning) & set(listOfSeqInKlotz)))
#         print( len(list(set(listOfSeqInNewPlanning) & set(listOfSeqInKlotz))))
#         
#         idSeq = 1
#         """The owner data will be modified accordingly"""
#         jd1Owner = "%.8f" % float(2456945.31600001)
#         jd2Owner = "%.8f" % float(2456945.32000001)
#         duration = (float(180)/86400.0)
#         priority = int(1)
#         sequence = Sequence(id=idSeq, owner=self.owner1, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration)
#         sequence.save()
#         
#         print( "New alert received ! Replanning ... ")
# #         sequence.display()
# 
#         self.planning.reschedule(2456945.30000001)
#         
#         self.planning.display()
# 
#         print( "The alert: ") 
#         sequence = list(Sequence.objects.filter(pk=1))[0]
#         sequence.display()
        
        
#     def test_PLAN_planner_Planning_schedule_planSequencesFromFile(self):
#         """
#         precond: sequences in database, empty planning
#         action: Test if the planning is correctly loaded with the sequences from the db
#         postcond: non empty planning
#         """
#         self.planning.initFromFile("planning.txt", self.owner1, self.quota1)  
#         self.planning.initFromDB(0, 3000000)
#         print( "Before"
#         self.planning.display()
#         self.planning.schedule()
# #         self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
#         print( "After"
#         self.planning.display()
# #         self.planning.displayGUI()        
        
        
        
    """Simple get from db tests"""    
     
        
    def test_PLAN_nonfunc_planner_Planning_schedule_initFromDB(self):
        """
        precond: 2 immediate sequences in planning from db
        action: Test if two simple immediate sequences are sorted in order
        postcond: sequence 1 is planned before sequence 2
         
        note:
        seq1.TSP < seq2.TSP and seq1.TEP < seq2.TEP and seq1.TEP <= seq2.TSP
        """
        self.s1.save()
        self.s2.save()
        self.planning.initFromDB(self.planStart, self.planEnd)
        self.planning.sequences = [self.s1, self.s2]
        self.planning.schedule()
        self.planning.display()
        #self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    
    
    """Complex delay tests"""
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleWithShiftLeftRight(self):
        """
        precond: 2 sequences
        action: Test if a third sequence can be inserted between two others
        postcond: the third sequence is planned between the first and second. The first and second must both move
          
        """  
        self.s1.delete()
        self.s2.delete()
        self.s17.save()
        self.s18.save()
        self.s1718.save()   
        self.planning.initFromDB(self.planStart, self.planEnd)
        self.planning.sequences = [self.s17, self.s18, self.s1718]
        self.planning.schedule()
        self.planning.display()
        #self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift()         
             
    
    """Non functional tests (ex: performance) """
    
#     def test_PLAN_nonfunc_planner_Planning_schedule_durationOfScheduling(self):   
#         """
#         precond: non empty planning
#         action: Test if the duration of schedule falls within requirements parameters
#         postcond: the executor time of the schedule function must be < X (TO DEFINE)
#           
#         note: 
#         This non functional test computes executor times and checks average, max and min of the durations
#         """ 
#             
#         myList = [] 
#         f = open('workfile.txt', 'r+')
#         for i in range(0,1000): 
# #             self.planning.initFromFile("planning.txt", self.owner1, self.quota1)    
#             self.planning.generateSequencesToFile(100)    
#             self.planning.planStart = 1
#             self.planning.planEnd = 1500
#             t0 = t.clock()
#             self.planning.schedule()
#             t1 = t.clock() 
#             del self.planning.intervals[:]
#             self.planning.intervals.append(Interval(self.planStart, self.planEnd, self.planEnd-self.planStart))        
#             del self.planning.sequences[:]
# #             del self.planning.sequencesHistory[:]
#             myList.append(t1-t0)           
#             f.write("Try: "+str(i)+" "+str(t0) + " " + str(t1) + " " + str(t1-t0) + "\n")      
#         f.write("\naverage: \n"+self.avg(myList))
#         f.write("\nmin: \n"+str(min(myList)))
#         f.write("\nmax: \n"+str(max(myList)))
#         f.close()
        
    
    """Multiple situation complex tests"""   
    
#     def test_PLAN_func_planner_Planning_schedule_multipleSequencesStatusPLANNED(self):
#         """
#         precond: non empty planning with lots of sequences of any type
#         action: Test if the duration of schedule falls within requirements parameters
#         postcond: The sequences must be all planned
#           
#         note: 
#         This tests checks to see if the various types of sequences are all planned
#         """        
#           
#         """clean up"""
#         self.s1.delete()
#         self.s2.delete()
#         self.s17.delete()
#         self.s18.delete()
#         self.s1718.delete()
#           
#         """set up """
#         self.s20.save()
#         self.s21.save()
#         self.s22.save()        
#         self.planning.initFromDB(1, 20)
#           
#         """scheduling"""
#         self.planning.schedule()
#           
#         """display results"""
#         self.planning.display()
#         self.planning.displayGUI()
#           
#         """assertions"""
        
    

if __name__ == '__main__':
    unittest.main()












