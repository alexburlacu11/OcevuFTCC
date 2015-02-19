import time
import copy
from os import listdir
from os.path import isfile, join
# import voeventparse




""" script which reads a folder and each time a voevent occurs it outputs it to the browser"""

    
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
        
                print(item)        
            
        self.old_files = self.new_files
        


if __name__ == '__main__':
       
    path = "D:\\shared\\voevents_received\\saved"
    interval = .1
    
    file_listener = FileListener(path, interval)   
    file_listener.start()   
        
    

