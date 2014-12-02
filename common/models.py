import socket
from SocketServer import *
import ConfigParser
from threading import Thread, Event
import os
import time
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
    
        
    def notifyObservers(self, message):
        if len(self.observers) == 0:
            print "No one listening"
        else:
            for observer in self.observers:
                data = observer.split(":")
                ip = data[0]
                port = data[1]
                print "sending "+message+" to "+ip+":"+str(port)
                self.send(message, ip, int(port))
                
    def send(self, message, ip, port):
        
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ip, port))
        clientsocket.send(message+"\n")
        data = clientsocket.recv(64)
        print "received data:", data
        clientsocket.close()
#         else:
#             print "No observers for "+self.name

            

        
         

class Agent(Thread):

    def __init__(self, agentName):
        self.status = "stopped"
        self.agentName = agentName
        self.ip = 'ip'
        self.sendPort = 0
        self.receivePort = 0
        self.sendBufferSize = 8192
        self.receiveBufferSize = 1024
        self.configFile = PROJECT_PATH + '\\'+'oft_config.ini'
        self.initFromConfigFile()
        self.sender = Sender(agentName+"Sender", self.ip, self.sendPort, self.sendBufferSize)
#         self.server = TCPServer((self.ip, self.receivePort), self.__class__.)
        self._stopevent = Event()
        self._sleepperiod = 1.0
        Thread.__init__(self, name=agentName)
        
    
#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(self.receiveBufferSize)
#         print self.data
#         self.analyseMessage(self.data)        
#         self.request.sendall("ok")       
            
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
        server.listen(1)
        
        while True:
            try:
                # Accept new connections.
                while True:
                    try:
                        conn, addr = server.accept()
                    except socket.error:
                        break
                    
                    conn.setblocking(False)
              
                    message = conn.recv(self.receiveBufferSize)                   
                    
                    self.analyseMessage(conn, message)
                    
                time.sleep(.1)
            except (SystemExit, KeyboardInterrupt):
                break
    
        
    
    def analyseMessage(self, conn, data):
        """analyse the message received in the socket"""
        
            
        
    def work(self):
        """do what the thread was built for""" 
        
    
    def display(self):
        print "Agent: "+str(self.agentName)+" is "+str(self.status)  
                
            
    def registerTo(self, agentName):
        print "registering to "+agentName
        ip, port = self.getAgentFromConfigFile(agentName)
        message = "register:"+ip+":"+str(self.receivePort)
        self.sender.send(message, ip, int(port))
                
        
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
        agentSection = self.agentName
        config = ConfigParser.ConfigParser()
        config.read(self.configFile)
        ip = config.get(agentSection,'ip')
        port = int(config.get(agentSection,'sendPort'))
        return ip, port
        
        
        
        
        
        
        
        
        
        
        
    
        
        
        
        
        