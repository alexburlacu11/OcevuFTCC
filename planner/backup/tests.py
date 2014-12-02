from django.test import TestCase

import unittest
from scheduling import Planning, Owner, Sequence, Quota
import time as t

class Test_Suite_for_Planner(unittest.TestCase):
    
    """Note: priority remains the same after initial sorting tests"""

    def setUp(self):
        """"
        Set up the environment. Create a new empty planning and some sequences. 
        Use test sequences to insert in planning according to the test objectives
        """
        self.planning = Planning( 0, [] , 0, 0, 0, 0)
        self.planStart = 1
        self.planEnd = 20
        self.owner1 = Owner("John", 'France', 60)
        self.quota1 = Quota(self.owner1, 100, 50,  60)
        """Immediate sequences"""
        self.s1 = Sequence(1, self.owner1, 3, 5, 2, 12, -1)
        self.s2 = Sequence(2, self.owner1, 7, 12, 5, 12, -1)    
        self.s3 = Sequence(3, self.owner1, 15, 18, 3, 12, -1) 
        self.s4 = Sequence(4, self.owner1, 18, 20, 2, 12, -1)       
        self.s6 = Sequence(6, self.owner1, 3, 5, 2, 12, -1)
        self.s7 = Sequence(7, self.owner1, 19, 20, 1, 13, -1)
        """Partially or completely overlapping immediate sequences"""
        self.s5 = Sequence(5, self.owner1, 3, 16, 6, 12, -1) 
        self.s5_1 = Sequence(51, self.owner1, 8, 16, 6, 12, -1)
        self.s5_2 = Sequence(52, self.owner1, 5, 16, 6, 12, -1)
        self.s5_3 = Sequence(53, self.owner1, 6, 18, 6, 12, -1)  
        self.s5_4 = Sequence(54, self.owner1, 4, 16, 6, 12, -1)   
        self.s5_5 = Sequence(55, self.owner1, 3, 16, 6, 12, -1)
        self.s5_6 = Sequence(56, self.owner1, 3, 15, 6, 12, -1)
        self.s5_7 = Sequence(57, self.owner1, 3, 15, 6, 12, -1)   
        self.s5_8 = Sequence(58, self.owner1, 3, 14, 6, 12, -1)
        self.s5_9 = Sequence(59, self.owner1, 3, 14, 6, 12, -1)   
        """Non immediate sequences"""
#         self.s5 = Sequence(5, self.owner1, 5, 8, 3, 12, 6)        
        self.s8 = Sequence(8, self.owner1, 5, 8, 3, 12, 6)
        self.s9 = Sequence(9, self.owner1, 10, 14, 3, 12, 13)
        self.s10 = Sequence(10, self.owner1, 16, 19, 3, 12, 17)
        """Overlapping sequences"""
        self.s11 = Sequence(11, self.owner1, 5, 14, 4, 12, 6)
        self.s12 = Sequence(12, self.owner1, 7, 14, 5, 12, 9)
        """Shifting sequences: don't use immediate sequences because they are non-shiftable"""
        """left"""
        self.s13 = Sequence(13, self.owner1, 1, 9, 6, 12, 6)
        self.s14 = Sequence(14, self.owner1, 13, 19, 6, 12, 16)
        self.s1314 = Sequence(1314, self.owner1, 1, 20, 6, 12, 11)
        """right"""
        self.s15 = Sequence(15, self.owner1, 3, 9, 6, 12, 6)
        self.s16 = Sequence(16, self.owner1, 14, 20, 4, 12, 16)
        self.s1516 = Sequence(1516, self.owner1, 12, 20, 4, 12, -1)
        """both left and right"""
        self.s17 = Sequence(17, self.owner1, 1, 8, 6, 12, 5)
        self.s18 = Sequence(18, self.owner1, 14, 20, 4, 12, 16)
        self.s1718 = Sequence(1718, self.owner1, 1, 20, 9, 12, 12 )
        """multiple sequences for simple tests without shift"""
        """check file"""
#         self.s201 = Sequence(201, self.owner1, 1, 2, 2, 12, -1)
        
        
        
    """Reusable tests and other functions"""   
    def subtest_PLAN_unit_planner_Planning_schedule_orderNSequences(self):
        """Check that all sequences are in the proper order"""
        numberOfSequences = len(self.planning.sequences)
        for i in xrange(0, numberOfSequences-1):
            self.assertLess(self.planning.sequences[i].TSP, self.planning.sequences[i+1].TSP)
            self.assertLess(self.planning.sequences[i].TEP, self.planning.sequences[i+1].TEP)
            self.assertLessEqual(self.planning.sequences[i].TEP, self.planning.sequences[i+1].TSP)
            
    def subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift(self):
        """Checks that the sequence following a shift is correctly placed"""
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
        
    
    """Init tests"""    
    
    
    def test_PLAN_unit_planner_Planning_initFromMemory(self):   
        """
        precond: No planning
        action: Load planning from memory and test if it has been instantiated
        postcond: Variables in planning must be instantiated
        """          
        self.planning.initFromMemory([self.s1, self.s2], self.planStart, self.planEnd)
        self.assertTrue(self.planning.sequences)
        self.assertTrue(self.planning.intervals)
        self.assertTrue(self.planning)
        
    def test_PLAN_unit_planner_Planning_initFromFile(self):
        """
        precond: File must exist
        action: Load planning from file and test if it has been instantiated 
        postcond: Variables in planning must be instantiated
        """       
        self.planning.initFromFile('planning.txt')
        self.assertTrue(self.planning.sequences)
        self.assertTrue(self.planning)   
        
    def test_PLAN_unit_planner_Planning_schedule_emptyPlanning(self):   
        """
        precond: Empty or no planning
        action: Test empty planning should fail because there are no sequences to schedule
        postcond: There should be no sequences in planning
        """              
        self.planning.schedule() 
        self.assertTrue(len(self.planning.sequences) == 0)    
    
            
    """Inserting sequences in planning"""
    
    def test_PLAN_unit_planner_Planning_schedule_checkTSPandTEPValuesAfterScheduling(self):
        """
        precond: new sequence in empty planning with jd1Owner = 3 and jd2Owner = 5
        action: Test if a sequence is given the proper plannification
        postcond: TSP = 3   TEP = 5
        """
        self.planning.initFromMemory([self.s1], self.planStart, self.planEnd)        
        self.planning.schedule()        
        self.assertTrue(self.s1.TSP == 3 )
        self.assertTrue(self.s1.TEP == 5 )
        

    def test_PLAN_unit_planner_Planning_schedule_insertSequenceInEmptyPlanning(self):
        """
        precond: Empty planning
        action: Test if a certain sequence is correctly inserted into an empty planning
        postcond: The inserted sequence should be found in the planning
        """
        self.planning.initFromMemory([self.s1], self.planStart, self.planEnd)
        self.planning.schedule() 
        self.assertTrue(self.planning.sequences[0] == self.s1)   
        
    def test_PLAN_unit_planner_Planning_schedule_insertSequenceInNonEmptyPlanning(self):
        """
        precond: Non empty planning with a planned sequence
        action: Test if a sequence is correctly inserted into a non empty planning
        postcond: The inserted sequence should be found in the planning
        """   
        self.planning.initFromMemory([self.s1], self.planStart, self.planEnd)
        self.planning.schedule()
        self.planning.sequences.append(self.s2)
        self.planning.schedule()
        self.assertTrue(self.planning.sequences[0] == self.s1)
        self.assertTrue(self.planning.sequences[1] == self.s2)
        self.assertTrue(len(self.planning.sequences) == 2)
        
    """Initial sorting tests: test priority and jd2Owner scheduling"""
        
    def test_PLAN_unit_planner_Planning_schedule_initialSort2Sequences(self):  
        """
        precond: 2 sequences of different jd2Owner in planning
        action: Test initial sorting according to the sequence priority and jd2Owner for 2 sequences
        postcond: The two sequences are ordered according to their priority first and then their jd2Owner
        """
        self.planning.initFromMemory([self.s1, self.s2], self.planStart, self.planEnd)        
        self.planning.schedule()        
        self.assertLessEqual(self.planning.sequences[0].sequencePriority, self.planning.sequences[1].sequencePriority)
        self.assertLess(self.planning.sequences[0].jd2Owner, self.planning.sequences[1].jd2Owner)
        
    def test_PLAN_unit_planner_Planning_schedule_initialSortMultipleSequences(self):   
        """
        precond: 4 sequences of different jd2Owner in planning
        action: Test sorting according to the sequence priority and jd2Owner for multiple sequences
        postcond: The 4 sequences are ordered according to their priority first and then their jd2Owner
        """
        self.planning.initFromMemory([self.s1, self.s2, self.s3, self.s4], self.planStart, self.planEnd)        
        self.planning.schedule()        
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
    
    """Scheduling tests for immediate sequences: test TSP, TEP, tPreference"""
               
    def test_PLAN_unit_planner_Planning_schedule_schedule2ImmediateSequencesSimple(self):
        """
        precond: 2 immediate sequences in planning
        action: Test if two simple immediate sequences are sorted in order
        postcond: sequence 1 is planned before sequence 2
        
        note:
        seq1.TSP < seq2.TSP and seq1.TEP < seq2.TEP and seq1.TEP <= seq2.TSP
        """
        self.planning.initFromMemory([self.s1, self.s2], self.planStart, self.planEnd)        
        self.planning.schedule()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()        
        
    def test_PLAN_unit_planner_Planning_schedule_scheduleMultipleImmediateSequencesSimple(self):
        """
        precond: 4 immediate sequences in planning
        action: Test if multiple simple sequences are sorted in order
        postcond: The sequences are sorted in order
        
        note: 
        seq1.TSP < seq2.TSP and seq1.TEP < seq2.TEP and seq1.TEP <= seq2.TSP .... etc
        """
        self.planning.initFromMemory([self.s1, self.s2, self.s3, self.s4], self.planStart, self.planEnd)        
        self.planning.schedule()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right same jd2Owner
        postcond: the second sequence is planned just after the end of the first
        
        note:
        seq5 has [ 3 , 16 ] with duration 6 -> [3 -> 9]
        seq5_1 has [ 8, 16 ] with duration 6 -> [9 -> 15]
           
        """
        self.planning.initFromMemory([self.s5,self.s5_1], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_2(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right same jd2Owner
        postcond: the second sequence is planned just after the end of the first
        
        note:
        seq5 has [ 3 , 16 ] with duration 6 -> [3 -> 9]
        seq5_2 has [ 5, 16 ] with duration 6 -> [9 -> 15]
           
        """
        self.planning.initFromMemory([self.s5,self.s5_2], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_3(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right different jd2Owner
        postcond: the second sequence is planned just after the end of the first
        
        note:
        seq5 has [ 3 , 16 ] with duration 6 -> [3 -> 9]
        seq5_3 has [ 6, 18 ] with duration 6 -> [9 -> 15]
           
        """
        self.planning.initFromMemory([self.s5,self.s5_3], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_4(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right same jd2Owner
        postcond: the second sequence is planned just after the end of the first
        
        note:
        seq5 has [ 3 , 16 ] with duration 6 -> [3 -> 9]
        seq5_3 has [ 6, 18 ] with duration 6 -> [9 -> 15]
                           
        """
        self.planning.initFromMemory([self.s5,self.s5_4], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_5(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that completely overlap are correctly planned, shift right
        postcond: The sequences are sorted in order
        
        note:
        The important thing here is that there is enough space after the plannification of the first
        sequence in order to plan the second. Which means that the duration of the first sequence plus
        the duration of the second sequence must be smaller thant jd2Owner. Otherwise, the test will fail
        seq5 has [ 3 , 16 ] with duration 6 -> [3 -> 9]
        seq5_5 has [ 3, 16 ] with duration 6 -> [9 -> 15]
           
        """
        self.planning.initFromMemory([self.s5,self.s5_5], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_6(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right
        postcond: the second sequence is planned just after the end of the first
        
        note:
        seq5_6 duration + seq5_7 duration <= jd2Owner
        seq5_6 has [ 3 , 15 ] with duration 6 -> [3 -> 9]
        seq5_7 has [ 3 , 15 ] with duration 6 -> [9 -> 15]
           
        """
        self.planning.initFromMemory([self.s5_6,self.s5_7], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()       
        self.assertTrue(self.planning.sequences[0].duration + self.planning.sequences[1].duration <= self.planning.sequences[0].jd2Owner)

    def test_PLAN_unit_planner_Planning_schedule_schedule2PartiallyOverlappingImmediateSequences_7(self):
        """
        precond: 2 partially overlapping immediate sequences
        action: Test if 2 sequences that partially overlap are correctly planned, shift right
        postcond: the second sequence is planned just after the end of the first
        
        note:
        This is the opposite of the above test, => seq5_6 duration + seq5_7 duration > jd2Owner so the
        second sequence should NOT be planned
        seq5_6 has [ 3 , 14 ] with duration 6 -> [3 -> 9]
        seq5_7 has [ 3 , 14 ] with duration 6 -> [????????] it will try to place the sequence with shift
           
        """
        self.planning.initFromMemory([self.s5_8,self.s5_9], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        """So we test that the second sequence was not planned"""
        self.assertTrue(self.planning.sequences[1].TSP == -1)
        self.assertTrue(self.planning.sequences[1].TEP == -1)
        """Added the jd1Owner of the first sequence because the sequence starts at 3 and not 0""" 
        self.assertTrue(self.planning.sequences[0].jd1Owner + self.planning.sequences[0].duration + self.planning.sequences[1].duration >= self.planning.sequences[1].jd2Owner)


    def test_PLAN_unit_planner_Planning_schedule_schedule2CompletelyOverlappingImmediateSequencesUnplanned(self):
        
        """
        precond: 2 overlapping immediate sequences
        action: Test if 2 sequences that completely overlap are correctly planned
        postcond: the second sequence is planned just after the end of the first
        
        note:
        Test if 2 sequences that overlap are correctly planned
        This test is exactly as the one above, the only difference being that there is not enough space between
        jd1Owner and jd2Owner for another sequence to be planned. 
        seq1 has [ 3 , 5 ] with duration 2 -> [3 -> 5]
        seq6 has [ 3, 5 ] with duration 2 -> [ ??????? ]
        It will not work because between 3 and 5 only one sequence of duration 2 can pe planned. The test
        must be modified to accept an interval of seq1 duration plus seq6 duration <= jd2Owner which is 5. 
        If we choose 7 instead of 5, the test will pass. 
        It will try to place s6 with a shift
        
        """
        self.planning.initFromMemory([self.s1,self.s6], self.planStart, self.planEnd)
        self.planning.schedule()
        """So we test that the second sequence was not planned"""
        self.assertTrue(self.planning.sequences[1].TSP == -1)
        self.assertTrue(self.planning.sequences[1].TEP == -1)
         
        
    """Non immediate sequences tests, simple = non-overlapping"""
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleSimpleNonImmediateSequences(self):
        """
        precond: 2 non-overlapping non-immediate sequences
        action: Test if 3 sequences that are not immediate are correctly planned
        postcond: the second sequence is planned just after the end of the first
        
        """
        self.planning.initFromMemory([self.s8, self.s9, self.s10], self.planStart, self.planEnd)
        self.planning.schedule()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    def test_PLAN_unit_planner_Planning_schedule_scheduleOverlappingNonImmediateSequences(self):
        """
        precond: 2 overlapping non immediate sequences
        action: Test if 2 sequences that are not immediate and are overlapping are correctly planned
        postcond: the second sequence is planned just after the end of the first
        
        """
        self.planning.initFromMemory([self.s11, self.s12], self.planStart, self.planEnd)
        self.planning.schedule()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
      
    """Delay/Shift tests"""
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleWithShiftLeftRight(self):
        """
        precond: 2 sequences
        action: Test if a third sequence can be inserted between two others
        postcond: the third sequence is planned between the first and second. The first and second must both move
        
        """     
        self.planning.initFromMemory([self.s17, self.s18, self.s1718], self.planStart, self.planEnd)
        self.planning.schedule()
        self.planning.display()
        self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift()          
        
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleWithShiftLeft(self):
        """
        precond: 2 sequences
        action: Test if a sequence moves to the left if a third sequence is to be scheduled between them
        postcond: the third sequence is planned between the first and second. The first must shift left
        
        """
        self.planning.initFromMemory([self.s13, self.s14, self.s1314], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift()
        
       
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleWithShiftRight(self):
        """
        precond: 2 sequences
        action: Test if a sequence moves to the right if a third sequence is to be scheduled between them
        postcond: the third sequence is planned between the first and second. The second must shift right
        
        """
        self.planning.initFromMemory([self.s15, self.s16, self.s1516], self.planStart, self.planEnd)
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_order3SequencesAfterShift() 
    
    
        
        
    """More complex tests"""
    
    def test_PLAN_unit_planner_Planning_schedule_scheduleWith2RealSequences(self):
        """
        precond: 2 sequences
        action: Test if sequences with real julian dates are correctly scheduled
        postcond: sequences are planned in the correct order
        
        """
        self.planning.initFromFile("planning.txt")
        self.planning.schedule()
#         self.planning.display()
#         self.planning.displayGUI()
        self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
        
    
    
    """Non functional tests (ex: performance) """
    
#     def test_PLAN_nonfunc_unit_planner_Planning_generateSequencesToFile_createRandomSequencesAndLoadInPlanning(self):
#         """
#         precond: Empty Planning
#         action: Test if sequences are generated in file and loaded in planning
#         postcond: nr of sequences equal to the value provided in tested function
#          
#         """
#                  
#         self.planning.generateSequencesToFile(100)
#         self.planning.initFromFile("planning.txt")
#         myList = []
#         f = open('workfile.txt', 'r+')
#         for i in xrange(0,10):       
#             t0 = t.clock()
#             self.planning.schedule()
#             t1 = t.clock() 
#             myList.append(t1-t0)           
#             f.write("Try: "+str(i)+" "+str(t0) + " " + str(t1) + " " + str(t1-t0) + "\n")      
#         f.write("\naverage: \n"+self.avg(myList))
#         f.write("\nmin: \n"+str(min(myList)))
#         f.write("\nmax: \n"+str(max(myList)))
#         f.close()
# #         self.planning.displayGUI()
#         self.subtest_PLAN_unit_planner_Planning_schedule_orderNSequences()
#           
#       
#     def test_PLAN_nonfunc_planner_Planning_schedule_durationOfScheduling(self):   
#         """
#         precond: non empty planning 
#         action: Test if the duration of schedule falls within requirements parameters
#         postcond: the execution time of the schedule function must be < X (TO DEFINE)
#          
#         note: 
#         This non functional test computes execution times and checks average, max and min of the durations
#         """      
#         self.planning.initFromMemory([self.s1, self.s2], self.planStart, self.planEnd) 
#         myList = []
#         f = open('workfile.txt', 'r+')
#         for i in xrange(0,10):       
#             t0 = t.clock()
#             self.planning.schedule()
#             t1 = t.clock() 
#             myList.append(t1-t0)           
#             f.write("Try: "+str(i)+" "+str(t0) + " " + str(t1) + " " + str(t1-t0) + "\n")      
#         f.write("\naverage: \n"+self.avg(myList))
#         f.write("\nmin: \n"+str(min(myList)))
#         f.write("\nmax: \n"+str(max(myList)))
#         f.close()
    

if __name__ == '__main__':
    unittest.main()












