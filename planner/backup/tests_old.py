'''
Created on Aug 20, 2014

@author: alex
'''

from scheduling import *


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
        s2 = Sequence(2, self.owner1, 7, 12, 5, 12, -1)
        s3 = Sequence(3, self.owner1, 15, 18, 3, 12, 15) 
        s4 = Sequence(4, self.owner1, 17, 19, 2, 12, 17)
        s5 = Sequence(5, self.owner1, 5, 8, 3, 12, 6)
#         sequences = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7]
        sequences = [s1, s2, s3, s4, s5]
        planStart = 1
        planEnd = 20
        plan = Planning( 'CLASSIC', sequences, s1, 1, planStart, planEnd)
        plan.schedule()
#         plan.displayGUI()
        
    def testLoadFromFile(self):
        """test File: Load planning from file"""
        print '---Test Files: Load planning from file'        
        plan = Planning( 0, None, 0, 0, 0, 0)
        print '-------Before------'
        plan.loadPlanningFromFile('planning.txt')
        plan.display()
        print '-------Scheduling------'        
        plan.schedule()
        print '-------After-------'
        plan.display()
        plan.displayGUI() 
        

def main():
    print "--------------Starting tests--------------"
    testSuite = Tests()
#     testSuite.test1a()   
#     testSuite.test1b()    
#     testSuite.test1c()
#     testSuite.test1d()
#     testSuite.test2a()
#     testSuite.test2b()
#     testSuite.testPlanPlot()
    testSuite.testLoadFromFile()

if __name__ == '__main__':
    main()