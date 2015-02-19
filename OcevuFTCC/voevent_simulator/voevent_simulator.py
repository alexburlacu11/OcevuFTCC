'''
Created on Dec 2, 2014

@author: alex
'''

from tornado import websocket, web, ioloop 
import json
import time
import os
import sys
import subprocess
from threading import Thread
import socket
import datetime
import configparser as ConfigParser
from tornado.web import asynchronous

import copy



clients = []

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OcevuFTCC.settings")
sys.path.append(BASE_DIR)

import alertManager
almn_path = os.path.abspath(alertManager.__path__[0])
import routineManager
romn_path = os.path.abspath(routineManager.__path__[0])
import planner
plan_path = os.path.abspath(planner.__path__[0])
import monitoring
moni_path = os.path.abspath(monitoring.__path__[0])
import executor
exec_path = os.path.abspath(executor.__path__[0])
import scientificDataManager
sdmn_path = os.path.abspath(scientificDataManager.__path__[0])

    

class IndexHandler(web.RequestHandler):
    @asynchronous
    def get(self):
        self.render("index.html")
         

class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        self.set_nodelay(True)
        if self not in clients:
            clients.append(self) 

    def on_close(self):
        if self in clients:
            clients.remove(self)
            

class SuperSTDOUTThread(Thread):
    
    def updateToWebPage(self, info):
        
        data = json.dumps(info)

        for client in clients:
            while True:
                try:                    
                    client.write_message(data)
                    break
                except Exception:
                    print ("Exception in sending data to web page") 
#                     print "Error sending data, retrying"
 
class SimulatorThread(SuperSTDOUTThread):
    def run(self):             
        sim = subprocess.Popen(["python", "file_listener.py"], stdout=subprocess.PIPE)
        for line in iter(sim.stdout.readline, b''):            
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]
            data = {"data": line}
            self.updateToWebPage(data)
            
            
                   
class CommandHandler(web.RequestHandler):
    
    @web.asynchronous
    def get(self, *args):
#         self.finish()
        command = self.get_argument("command")
        print ("["+str(datetime.datetime.now())+"]"+"Received ajax command: "+command)   
        if command == "go":
            sim = SimulatorThread()
            sim.start()
#             time.sleep(.1)

class VOEventHandler(web.RequestHandler, SuperSTDOUTThread):
    
    @web.asynchronous
    def get(self, *args):
        self.finish()
        title = self.get_argument("title")
        print ("["+str(datetime.datetime.now())+"]"+"Received request for voevent: "+title)
        
        """ search for the file by id in the directory and output it to the page """
        v = 'D:\\shared\\voevents_received\\saved\\'+title        
        
#         self.display_info(v)    
        
        from lxml import etree
        tree=etree.parse(v)
        
        info = ''      
        for child in tree.iter():
            info += str(child.tag) +": "+str(child.attrib)+": "+str(child.text)+"<br>"
        
        
        data = {"details": info }
        self.updateToWebPage(data)
    
#     def display_info(self, v):       

         
#         with open(fi, 'rb') as f:
#             v = voeventparse.load(f)
#              
#         data = {"details": v}
#         self.updateToWebPage(data)
         
#         #Basic attribute access
#         print("Ivorn:", v.attrib['ivorn'])
#         print("Role:", v.attrib['role'])
#         print( "AuthorIVORN:", v.Who.AuthorIVORN)
#         print( "Short name:", v.Who.Author.shortName)
#         print( "Contact:", v.Who.Author.contactEmail)
#         
#         #Copying by value, and validation:
#         print( "Original valid as v2.0? ", voeventparse.valid_as_v2_0(v))
#         v_copy = copy.copy(v)
#         print( "Copy valid? ", voeventparse.valid_as_v2_0(v_copy))
#         
#         #Changing values:
#         v_copy.Who.Author.shortName = 'BillyBob'
#         v_copy.attrib['role'] = voeventparse.definitions.roles.test
#         print( "Changes valid? ", voeventparse.valid_as_v2_0(v_copy))
#         
#         v_copy.attrib['role'] = 'flying circus'
#         print( "How about now? ", voeventparse.valid_as_v2_0(v_copy))
#         print( "But the original is ok, because we copied? ", voeventparse.valid_as_v2_0(v))
#         
#         v.Who.BadPath = "This new attribute certainly won't conform with the schema."
#         assert voeventparse.valid_as_v2_0(v) == False
#         del v.Who.BadPath
#         assert voeventparse.valid_as_v2_0(v) == True
#         #######################################################
#         # And now, SCIENCE
#         #######################################################
#         c = voeventparse.pull_astro_coords(v)
#         print( "Coords:", c)
                        

    
class ConsoleHandler(web.RequestHandler):   

    @web.asynchronous
    def get(self, *args): 
        self.finish()

    @web.asynchronous
    def post(self):
        pass
    
    

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/console', ConsoleHandler),
    (r'/command', CommandHandler),
    (r'/voevent', VOEventHandler),

    
       
])

if __name__ == '__main__':
    app.listen(8002)
    print ("VoEvent simulator started on 8002")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OcevuFTCC.settings")
    ioloop.IOLoop.instance().start()
    
    
     
    
    