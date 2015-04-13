import time
import copy
from os import listdir
from os.path import isfile, join
# import voeventparse
import os



MODE_NASA = True

PATH_WINDOWS = "voevents_received/saved/"
PATH_MAC = "/projects/f-gft-cc/SOFT/eclipse_workspace/fgft_cc/fgft_cc/voevent_simulator/voevents_received/saved/"
PATH_LINUX = "voevents_received/saved/"


if os.name == "nt":
    PATH = PATH_WINDOWS
else:
    if os.name == "mac":
        PATH = PATH_MAC
    else:
        PATH = PATH_LINUX

    
class FileListener:
    
    def __init__(self, folder_path, interval):
        self.path = folder_path
        self.old_files = []
        self.new_files = []
        self.interval = interval

    def start(self):   
        
        while True:                   
            
            file_listener.check_for_new_file()     
        
            time.sleep(self.interval)
    
    
    def check_for_new_file(self):
        
        self.new_files = [ f for f in listdir(self.path) if isfile(join(self.path,f)) ]    
        
        diff = list(set(self.new_files).difference(set(self.old_files)))
        
        if len(diff) != 0:
            
            for item in diff:
        
                if item != "voevent.xml":
                
                    print(item)        
            
        self.old_files = self.new_files
        


if __name__ == '__main__':
       
    
    interval = .1
    
    file_listener = FileListener(PATH, interval)   
    file_listener.start()   
        
    

