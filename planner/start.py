
'''
Created on Nov 7, 2014

@author: alex

class Planning Controller

'''




import django 
import os
import sys
 
if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fgft_cc.settings")
    sys.path.append(BASE_DIR) 
    
    from planner.models import PlanningController
   
    controller = PlanningController()    
    controller.start()
    
        