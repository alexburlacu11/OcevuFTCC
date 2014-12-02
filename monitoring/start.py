'''
Created on Nov 7, 2014

@author: alex

class Monitoring Controller

'''


from monitoring.models import MonitoringController 

if __name__ == '__main__':
    
    controller = MonitoringController()    
    controller.start()
    

