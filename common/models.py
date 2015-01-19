import socket

import configparser as ConfigParser
from threading import Thread, Event
import os
import time
import datetime
from random import randint
from decimal import Decimal
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


class Sender(Thread): 
    def __init__(self, agentName, ip, port, sendBufferSize):
        self.agentName = agentName
        self.ip = ip
        self.receivePort = port
        self.sendBufferSize = sendBufferSize
        self.observers = []
        Thread.__init__(self, name=agentName)        
        
    def run(self):
        """Servers send different things"""   
        print( "["+str(datetime.datetime.now())+"]"+self.agentName+" started")
        self.work()
        
    def work(self):
        """Create the type of data to be sent to observers"""
    
        
    def notifyObservers(self, message):
        if len(self.observers) == 0:
            print( "["+str(datetime.datetime.now())+"]"+"No one listening")
        else:
            for observer in self.observers:
                data = observer.split(":")
                ip = data[0]
                port = data[1]
                print( "["+str(datetime.datetime.now())+"]"+"Sending "+message+" to "+ip+":"+str(port))
                self.send(message, ip, int(port))
                
    def send(self, message, ip, port):
         
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ip, port))
        clientsocket.send(message+"\n")
        data = clientsocket.recv(64)
        print( "["+str(datetime.datetime.now())+"]"+"Received data: ", data)
        clientsocket.close()
#         else:
#             print( "["+str(datetime.datetime.now())+"]"+"No observers for "+self.name

            
    
        
         

class Agent(Thread):

    def __init__(self, agentName):
        self.status = "stopped"
        self.agentName = agentName
        self.ip = 'ip'
        self.sendPort = 0
        self.receivePort = 0
        self.sendBufferSize = 8192
        self.receiveBufferSize = 8192
        self.configFile = PROJECT_PATH + '\\'+'oft_config.ini'
        self.initFromConfigFile()
        self.sender = Sender(agentName+" Sender", self.ip, self.sendPort, self.sendBufferSize)
        self._stopevent = Event()
        self._sleepperiod = 1.0
        Thread.__init__(self, name=agentName)
      
            
    def run(self):
        """each controller thread will behave differently"""        
        self.work()    
        self.sender.start()
        self.receive()
#         self.server.serve_forever()
        
    def start(self):
        """loop which accepts connections"""
        self.status = "running"
        self.display()  
        Thread.start(self)
        
    def stop(self):
        """stops the agent"""
        self.status = "stopped"
        self.display()
        self._stopevent.set()
        Thread.join(self, None)
        
            
    def receive(self):  
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(False)
        server.bind((self.ip, self.receivePort))
        server.listen(12)
        
        while True:
            try:
                # Accept new connections.
                while True:
                    try:
                        conn, addr = server.accept()
                    except socket.error:
                        break
                    
                    conn.setblocking(False)
              
                    data = conn.recv(self.receiveBufferSize)     
                    
                    data = data.rstrip('\n')
                    print( "["+str(datetime.datetime.now())+"]"+self.agentName+" received : "+data )                     
                    
                    self.analyseMessage(conn, data)
                    
                time.sleep(.1)
            except (SystemExit, KeyboardInterrupt):
                break
    
        
    
    def analyseMessage(self, conn, data):
        
        """analyse the message received in the socket"""       
             
        dataSet = data.split(":")
        rtype = dataSet[0]
        ip = dataSet[1]
        port = dataSet[2]
        if rtype == "register":
            obs = [o for o in self.sender.observers if o == ip+":"+str(port)]
            if len(obs) == 0:
                print( "["+str(datetime.datetime.now())+"]"+"New client registered")
                self.addObserver(ip+":"+str(port))
                conn.send("ok\n")
            else:
                print( "["+str(datetime.datetime.now())+"]"+"Client already registered")
                conn.send("Already registered\n")
        
            
        
    def work(self):
        """do what the thread was built for""" 
        
    
    def display(self):
        print( "["+str(datetime.datetime.now())+"]"+str(self.agentName)+" is "+str(self.status)+" on "+str(self.ip)+":"+str(self.receivePort))  
                
            
    def registerTo(self, agentName):
        print( "["+str(datetime.datetime.now())+"]"+self.agentName+" is registering to "+agentName)
        ip, receivePort = self.getAgentFromConfigFile(agentName)
        message = "register:"+self.ip+":"+str(self.receivePort)
#         print( "["+str(datetime.datetime.now())+"]"+message+" will be sent to "+str(ip)+":"+str(receivePort)
        self.sender.send(message, ip, int(receivePort))
                
        
    """observer-observable behaviour"""
        
    def addObserver(self, observer): 
        self.sender.observers.append(observer)
        
    def removeObserver(self, observer):
        self.sender.observers.remove(observer)
        
           
    """configuration functions"""
    
    def initFromConfigFile(self):
        """initiate agent from the ini file in common"""
        agentSection = self.agentName
        config = ConfigParser.ConfigParser()
        config.read(self.configFile)
        self.agentName = config.get(agentSection,'agentName')
        self.ip = config.get(agentSection,'ip')
        self.sendPort = int(config.get(agentSection,'sendPort'))
        self.receivePort = int(config.get(agentSection,'receivePort'))
        
    def getAgentFromConfigFile(self, name):
        agentSection = name
        config = ConfigParser.ConfigParser()
        config.read(self.configFile)
        ip = config.get(agentSection,'ip')
        port = int(config.get(agentSection,'receivePort'))
#         print( "["+str(datetime.datetime.now())+"]"+"DEBUG: getAgentFromConfigFile: "+str(ip)+":"+str(port)
        return ip, port
        
        
class OFTThreadManager():
    
    @staticmethod   
    def getJd1Jd2(location):
        
        import subprocess

        p = subprocess.Popen(["/home/oftcc/git/ext/jd1jd2_Cpp_V1.0/astro", "-o", "Toulouse"], stdout=subprocess.PIPE)

        a =  p.communicate()

        values = a[0].split()  
        
        jd1 = values[2]
        jd2 = values[5]
        data = [ jd1, jd2 ]        
        
        return data
    
    @staticmethod   
    def getConsoleOutput():
        import os
        import time
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        
        import subprocess

        monitoring = subprocess.Popen(["python", BASE_DIR+"\\"+"monitoring\s.py"], stdout=subprocess.PIPE)
        time.sleep(1)
        planning = subprocess.Popen(["python", BASE_DIR+"\\"+"planner\s.py"], stdout=subprocess.PIPE)
 
        a =  monitoring.communicate()
        b = planning.communicate()
                 
        c1 = a
        c2 = b
        
        data = [ c1,c2 ]        
        
        return data     
        
        
        
        
        
        
        
        
    
        
        
        
        
        