'''
Created on Dec 15, 2014

@author: alex
'''

 
import django 
import os
import sys
 
if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fgft_cc.settings")
    sys.path.append(BASE_DIR) 

    from models import ExecutionController  
    controller = ExecutionController()    
    controller.start() 