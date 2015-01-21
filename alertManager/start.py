'''
Created on Nov 7, 2014

@author: alex

class Monitoring Controller

'''

import django

from alertManager.models import AlertManagerController 

if __name__ == '__main__':
    django.setup()
    controller = AlertManagerController()    
    controller.start()
    

