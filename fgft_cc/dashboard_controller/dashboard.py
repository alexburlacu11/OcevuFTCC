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



clients = []

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fgft_cc.settings")
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
            
class MonitoringThread(SuperSTDOUTThread):
    def run(self):             
        monitoring = subprocess.Popen(["python", os.path.join(moni_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(monitoring.stdout.readline, b''):            
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]
            data = {"moni": line}
            self.updateToWebPage(data)
                
class PlanningThread(SuperSTDOUTThread):
    def run(self):             
        planning = subprocess.Popen(["python", os.path.join(plan_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(planning.stdout.readline, b''):  
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]          
            data = {"plan": line}
            self.updateToWebPage(data)
            
class AlertThread(SuperSTDOUTThread):
    def run(self):             
        alertManager = subprocess.Popen(["python", os.path.join(almn_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(alertManager.stdout.readline, b''):            
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]
            data = {"almn": line}
            self.updateToWebPage(data)
                
class RoutineThread(SuperSTDOUTThread):
    def run(self):             
        routineManager = subprocess.Popen(["python", os.path.join(romn_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(routineManager.stdout.readline, b''): 
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]           
            data = {"romn": line}
            self.updateToWebPage(data)
            
class ExecThread(SuperSTDOUTThread):
    def run(self):             
        execution = subprocess.Popen(["python", os.path.join(exec_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(execution.stdout.readline, b''):          
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]  
            data = {"exec": line}
            self.updateToWebPage(data)
            
class ScientificDataManagementThread(SuperSTDOUTThread):
    def run(self):             
        sdmn = subprocess.Popen(["python", os.path.join(sdmn_path,"start.py")], stdout=subprocess.PIPE)
        for line in iter(sdmn.stdout.readline, b''):  
            line = str(line).replace('"', '').replace("'", '').rstrip('\\n').rstrip('\\r')[1:]          
            data = {"sdmn": line}
            self.updateToWebPage(data)


class AlertHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        command = self.get_argument("command")
        if command=="start":
            alert = AlertThread()
            alert.start()
            time.sleep(.1)

        
class MonitoringHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        moni = MonitoringThread()
        moni.start()
        time.sleep(.1)  
        
class RoutineHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        routine = RoutineThread()
        routine.start()
        time.sleep(.1)
        

        
class ExecHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        execution = ExecThread()
        execution.start()
        time.sleep(.1)
        
class PlanHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        plani = PlanningThread()      
        plani.start()
        time.sleep(.1)
        
class SDMNHandler(web.RequestHandler):
    
    @web.asynchronous
    def get (self, *args):
        sdmn = ScientificDataManagementThread()
        sdmn.start()
        time.sleep(.1)

class CommandHandler(web.RequestHandler):
    
    @web.asynchronous
    def get(self, *args):
        self.finish()
        configFile = BASE_DIR+"\\"+"common\oft_config.ini"
        command = self.get_argument("command")

        print ("["+str(datetime.datetime.now())+"]"+"Received ajax command: "+command)
        if command == "alert_sim":
            """send socket to alertManager to create a new sequence and notify observers"""
            message = "alert_sim"
            ip, port = self.getAgentFromConfigFile("AlertManager", configFile)
            self.send(message, ip, port)
        else:
            if command == "request_sim":
                message = "request_sim"
                ip, port = self.getAgentFromConfigFile("RoutineManager", configFile)
                self.send(message, ip, port)
            else:
                if command == "obs_sim":
                    message = "obs_sim"
                    ip, port = self.getAgentFromConfigFile("Monitoring", configFile)
                    self.send(message, ip, port)
                    
        
            
        
    def send(self, message, ip, port):        
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ip, port))
        clientsocket.send(bytes(message, 'UTF-8'))
        data = clientsocket.recv(64).decode()
        print ("["+str(datetime.datetime.now())+"]"+"Received data: ", data)
        clientsocket.close()
        return 
        
    def getAgentFromConfigFile(self, name, configFile):
        agentSection = name
        config = ConfigParser.ConfigParser()
        config.read(configFile)
        ip = config.get(agentSection,'ip')
        port = int(config.get(agentSection,'receivePort'))
#         print "["+str(datetime.datetime.now())+"]"+"DEBUG: getAgentFromConfigFile: "+str(ip)+":"+str(port)
        return ip, port
        

class ConsoleHandler(web.RequestHandler):   

    @web.asynchronous
    def get(self, *args): 
        self.finish()     
        
        """
        show first three sequences in planning to see if planning is ok for an alert when it arrives or routine req
         """
        
        

    @web.asynchronous
    def post(self):
        pass

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/console', ConsoleHandler), 
    (r'/almn', AlertHandler),
    (r'/romn', RoutineHandler),
    (r'/moni', MonitoringHandler),
    (r'/exec', ExecHandler),
    (r'/plan', PlanHandler),
    (r'/sdmn', SDMNHandler),
    (r'/command', CommandHandler),

    
       
])

if __name__ == '__main__':
    app.listen(8001)
    print ("Tornado server started on 8001")
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fgft_cc.settings")
    sys.path.append(BASE_DIR)
    ioloop.IOLoop.instance().start()
    
    
     
    
    