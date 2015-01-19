'''
Created on Dec 2, 2014

@author: alex
'''
from tornado import websocket, web, ioloop
import json
import time
import os
import subprocess
from threading import Thread
import socket
import datetime
import ConfigParser

clients = []
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class IndexHandler(web.RequestHandler):
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
    
    def updateToWebPage(self, data):
        data = json.dumps(data, ensure_ascii=False)
        for client in clients:
            while True:
                try:
                    
                    client.write_message(data)
                    break
                except Exception:
                    print Exception.message 
#                     print "Error sending data, retrying"
            
class MonitoringThread(SuperSTDOUTThread):
    def run(self):             
        monitoring = subprocess.Popen(["python", BASE_DIR+"\\"+"monitoring\start.py"], stdout=subprocess.PIPE)
        for line in iter(monitoring.stdout.readline, b''):            
            data = {"moni": line}
            self.updateToWebPage(data)
                
class PlanningThread(SuperSTDOUTThread):
    def run(self):             
        planning = subprocess.Popen(["python", BASE_DIR+"\\"+"planner\start.py"], stdout=subprocess.PIPE)
        for line in iter(planning.stdout.readline, b''):            
            data = {"plan": line}
            self.updateToWebPage(data)
            
class AlertThread(SuperSTDOUTThread):
    def run(self):             
        alertManager = subprocess.Popen(["python", BASE_DIR+"\\"+"alertManager\start.py"], stdout=subprocess.PIPE)
        for line in iter(alertManager.stdout.readline, b''):            
            data = {"almn": line}
            self.updateToWebPage(data)
                
class RoutineThread(SuperSTDOUTThread):
    def run(self):             
        routineManager = subprocess.Popen(["python", BASE_DIR+"\\"+"routineManager\start.py"], stdout=subprocess.PIPE)
        for line in iter(routineManager.stdout.readline, b''):            
            data = {"romn": line}
            self.updateToWebPage(data)
            
class ExecThread(SuperSTDOUTThread):
    def run(self):             
        execution = subprocess.Popen(["python", BASE_DIR+"\\"+"execution\start.py"], stdout=subprocess.PIPE)
        for line in iter(execution.stdout.readline, b''):            
            data = {"exec": line}
            self.updateToWebPage(data)
            
class ScientificDataManagementThread(SuperSTDOUTThread):
    def run(self):             
        sdmn = subprocess.Popen(["python", BASE_DIR+"\\"+"scientificDataManager\start.py"], stdout=subprocess.PIPE)
        for line in iter(sdmn.stdout.readline, b''):            
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
        print "received command ajax"
        configFile = BASE_DIR+"\\"+"common\oft_config.ini"
        command = self.get_argument("command")
        command = command.rstrip('\n')
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
        clientsocket.send(message+"\n")
        data = clientsocket.recv(64)
        print "["+str(datetime.datetime.now())+"]"+"Received data: ", data
        clientsocket.close()
        
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
    print "Tornado started on 8001"
    ioloop.IOLoop.instance().start()
    
    
    
    
    