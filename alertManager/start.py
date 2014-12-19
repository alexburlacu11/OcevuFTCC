'''
Created on Nov 7, 2014

@author: alex

class Monitoring Controller

'''


from alertManager.models import AlertManagerController 

if __name__ == '__main__':
    
    controller = AlertManagerController()    
    controller.start()
    

