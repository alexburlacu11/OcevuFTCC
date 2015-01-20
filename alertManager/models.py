import copy
import datetime
from decimal import Decimal
import getopt 
import os
import os
from random import randint
import sys
from uuid import uuid4

from django.db import models
from lxml import etree as ET 
  
import alertManager.VOEventLib.VOEvent 
import alertManager.VOEventLib.Vutil
from alertManager.VOEventLib import Vutil
from alertManager.VOEventLib.VOEvent import usage
from alertManager.VOEventLib.original.format_to_html import display, \
    format_to_stdout, format_to_file, format_to_string
from common.models import Agent, Sender
from planner.models import Sequence, Owner


try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
   

class AlertManagerSender(Sender):   
    
#     def work(self):
#         while True:
#             
#             """create some fake sequences here"""
#             self.createFakeSequence("Alert")
#             
#             message = "alert"
#             
#             self.notifyObservers(message)                                  
#             time.sleep(10)
            
    def createFakeSequence(self, data):
#         owner = Owner(name=data)
#         owner.save()
#         idSeq = 1                       
#         jd1Owner = 2456981.68341667
#         jd2Owner = 2456981.73684001
#         duration = jd2Owner-jd1Owner
#         priority = 1
#         darkness = 11
#         sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration, darkness=darkness)
#         sequence.save()
               
        
        n = randint(1,1000)
        owner = Owner(name=data)
        owner.save()
        idSeq = n
        n1 = str(randint(100000, 999999))             
        n2 = str(randint(100000, 999999))          
        jd1Owner = Decimal(str(2456981.68)+n1)
        jd2Owner = Decimal(str(2456981.73)+n2)
        duration = jd2Owner-jd1Owner
        priority = 1
        darkness = Decimal(11)
        sequence = Sequence(id=idSeq, owner=owner, jd1Owner=jd1Owner, jd2Owner=jd2Owner, priority=priority, duration=duration, darkness=darkness)
        sequence.save()
        
    
        

class AlertManagerController(Agent):
    
    def __init__(self):
        Agent.__init__(self, 'AlertManager')
        self.sender = AlertManagerSender(self.agentName+" Sender", self.ip, self.receivePort, self.sendBufferSize)
      
    def analyseMessage(self, conn, data):
        
        if data == "alert_sim":            
            message = "alert"
            self.sender.createFakeSequence("AlertSim")
            self.sender.notifyObservers(message)
            conn.send(bytes("ok", 'UTF-8'))
        else:
            Agent.analyseMessage(self, conn, data) 
    
   
class Alert(models.Model):
    ivorn = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True,)
    
    def get_absolute_url(self):
        return "/alertmanager/view/%i/" % self.id

#     importance = models.FloatField(null=True, blank=True,)
#     expires = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
#     observation_astro_coord_system_id = models.IntegerField(null=True, blank=True,)
#     observation_time = models.DateTimeField('observation_time',null=True, blank=True,)
#     observation_time_unit = models.CharField(max_length=100)
#     observation_time_error = models.DateTimeField('observation_time_error',null=True, blank=True,)
#     position_2d_value_1 = models.FloatField(null=True, blank=True,)
#     position_2d_value_2 = models.FloatField(null=True, blank=True,)
#     position_2d_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_2d_error2radius = models.FloatField(null=True, blank=True,)
#     observatory_id = models.IntegerField(null=True, blank=True,)
#     observatory_astro_coord_system_id = models.IntegerField(null=True, blank=True,)
#     position_3d_value_1 = models.FloatField(null=True, blank=True,)
#     position_3d_value_2 = models.FloatField(null=True, blank=True,)
#     position_3d_value_3 = models.FloatField(null=True, blank=True,)
#     position_3d_value1_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_3d_value2_unit = models.CharField(max_length=20,null=True, blank=True,)
#     position_3d_value3_unit = models.CharField(max_length=20,null=True, blank=True,)
   
    def display(self, source, o=sys.stdout):
        '''Generate HTML that provides a display of an event.
        '''
        v = Vutil.parse(source)
        print( '' )
        print( 'IVORN <i>%s</i><br/>' % v.get_ivorn())
        print( '(role is %s)' % v.get_role())
    
        print( '<p>Event description: %s</p>\n' % v.get_Description())
    
        r = v.get_Reference()
        if r:
            print( 'Reference<br/>Name=%s, Type=%s, uri=%s' \
                        % (r.get_name(), r.get_type(), r.get_uri()))
        print( '<h3>Who</h3>')
        who = v.get_Who()
        a = who.get_Author()
        print( 'Title: %s'                        % Vutil.htmlList(a.get_title()))
        print( 'Name: %s'                         % Vutil.htmlList(a.get_contactName()))
        print( 'Email: %s'                        % Vutil.htmlList(a.get_contactEmail()))
        print( 'Phone: %s'                        % Vutil.htmlList(a.get_contactPhone()))
        print( 'Contributor: %s<br/>' % Vutil.htmlList(a.get_contributor()))
        print( '<h3>What</h3>')
        print( '<h4>Params</h4>')
        print( '<table border="1"><tr>')
        print( '<td>Group</td>')
        print( '<td>Name</td>')
        print( '<td>Description</td>')
        print( '<td><b>Value</b></td>')
        print( '<td>ucd</td>')
        print( '<td>unit</td>')
        print( '<td>dataType</td>')
        print( '</tr>')
        g = None
        params = v.get_What().get_Param()
        for p in params:
            print( '<tr>' + Vutil.htmlParam(g, p) + '</tr>')
    
        groups = v.get_What().get_Group()
        for g in groups:
            for p in g.get_Param():
                print( '<tr>' + Vutil.htmlParam(g, p) + '</tr>')
        print( '</table>')
        print( '<h4>Tables</h4>')
        tables = v.get_What().get_Table()
        for t in tables:
            print( '<table border="1">')
    
            print( '<tr><td><i>Name</i></td>')
            for f in t.get_Field():
                print( '<td>' + str(f.get_name()) + '</td>')
            print( '</tr>')
    
            print( '<tr><td><i>UCD</i></td>')
            for f in t.get_Field():
                print( '<td>' + str(f.get_ucd()) + '</td>')
            print( '</tr>')
    
            print( '<tr><td><i>unit</i></td>')
            for f in t.get_Field():
                print( '<td>' + str(f.get_unit()) + '</td>')
            print( '</tr>')
            print( '<tr><td><i>dataType</i></td>')
            for f in t.get_Field():
                print( '<td>' + str(f.get_dataType()) + '</td>')
            print( '</tr>')
            print( '<tr><td/></tr>')
            d = t.get_Data()
            if d:
                for tr in d.get_TR():
                    print( '<tr><td/>')
                    for td in tr.get_TD():
                        print( '<td>' + td + '</td>')
                    print( '</tr>')
            print( '</table>')
        print( '<h3>WhereWhen</h3>')
        wwd = Vutil.whereWhenDict(v)
        if wwd:
            print( '<table border="1">')
            print( '<tr><td>Observatory</td> <td>%s</td></tr>' % wwd['observatory'])
            print( '<tr><td>Coord system</td><td>%s</td></tr>' % wwd['coord_system'])
            print( '<tr><td>Time</td>                <td>%s</td></tr>' % wwd['time'])
            print( '<tr><td>Time error</td>  <td>%s</td></tr>' % wwd['timeError'])
            print( '<tr><td>RA</td>                  <td>%s</td></tr>' % wwd['longitude'])
            print( '<tr><td>Dec</td>                 <td>%s</td></tr>' % wwd['latitude'])
            print( '<tr><td>Pos error</td>       <td>%s</td></tr>' % wwd['posError'])
            print( '</table>')
        print( '<h3>Why</h3>')
        w = v.get_Why()
        if w:
            if w.get_Concept():
                print( "Concept: %s" % Vutil.htmlList(w.get_Concept()))
            if w.get_Name():
                print( "Name: %s"        % Vutil.htmlList(w.get_Name()))
    
            print( '<h4>Inferences</h4>')
            inferences = w.get_Inference()
            for i in inferences:
                print( '<table border="1">')
                print( '<tr><td>probability</td><td>%s</td></tr>' % i.get_probability())
                print( '<tr><td>relation</td>     <td>%s</td></tr>' % i.get_relation())
                print( '<tr><td>Concept</td>      <td>%s</td></tr>' % Vutil.htmlList(i.get_Concept()))
                print( '<tr><td>Description</td><td>%s</td></tr>' % Vutil.htmlList(i.get_Description()))
                print( '<tr><td>Name</td>             <td>%s</td></tr>' % Vutil.htmlList(i.get_Name()))
                print( '<tr><td>Reference</td>  <td>%s</td></tr>' % str(i.get_Reference()))
                print( '</table>')
        print( '<h3>Citations</h3>')
        cc = v.get_Citations()
        if cc:
            for c in cc.get_EventIVORN():
                print( '<ul>')
                print( '<li>%s with a %s</li>' % (c.get_valueOf_(), c.get_cite()))
                print( '</ul>')
        print( '' )
    
    
    def format_to_stdout(self, infilename):
        '''Write HTML to standard output.
        '''
        display(infilename)
    
     
    def format_to_file(self,infilename, outfilename, force):
        '''Write HTML to a file.
        
        Check for existence of the file.  If it exists,
        write only if force is True.
        '''
        if os.path.exists(outfilename) and not force:
            sys.stderr.write(
                '\nFile %s exists.  Use -f/--force to over-write.\n\n' % (
                outfilename, ))
            sys.exit(1)
        outfile = open(outfilename, 'w')
        display(infilename, outfile)
        outfile.close()
    
        
    def format_to_string(self, infilename):
        '''Format as HTML and capture in a string.  Return the string.
        '''
        outfile = StringIO()
        display(infilename, outfile)
        content = outfile.getvalue()
        return content
    
    def format_to_html(self,infilename):
        '''Format as HTML and capture in a string.  Return the string.
        '''
        outfilename = 'q'
        outfile = open(outfilename, 'w')
        self.display(infilename, outfile)
        outfile.close()
        with open (outfilename, "r") as myfile:
            content=myfile.read()
            
        return content
    
    
    def usage(self):
        sys.stderr.write(__doc__)
        sys.exit(1)
    
    
    def main_old(self):
        args = sys.argv[1:]
        try:
            opts, args = getopt.getopt(args, 'hso:tf', ['help',
                'stdout', 'outfile=', 'text', 'force' ])
        except:
            usage()
        outfilename = None
        stdout = False
        force = False
        text = False
        for opt, val in opts:
            if opt in ('-h', '--help'):
                usage()
            elif opt in ('-o', '--outfile'):
                outfilename = val
            elif opt in ('-s', '--stdout'):
                stdout = True
            elif opt in ('-t', '--text'):
                text = True
            elif opt in ('-f', '--force'):
                force = True
        if len(args) != 1:
            usage()
        infilename = args[0]
        if stdout:
            format_to_stdout(infilename)
        if outfilename is not None:
            format_to_file(infilename, outfilename, force)
        if text:
            content = format_to_string(infilename)
            print( "["+str(datetime.datetime.now())+"]"+content )
        if not stdout and outfilename is None and not text:
            usage()
            
    def get(self, id_):        
        v = Alert.objects.get(pk=id_)
        return v
    
    def getByID(self, id):
        a = Alert.objects.filter(pk=id)
        return a
    
    def getByIvorn(self, ivorn_):        
        v = Alert.objects.get(ivorn=ivorn_)
        return v
    
    def getAll(self):        
        v = Alert.objects.all().order_by('-date')
        return v
        
    def loadVOEventFromXML(self, xml_filename):           
        
        with open (xml_filename, "r") as myfile:
            data=myfile.read()
            
#         v = voeparse.loads(data, False)
        
#         alert = Alert(
#                            ivorn=v.attrib['ivorn'],
#                            author=v.Who.Author.shortName,
#                            
#                            
#                           )
#         '''
#         TODO: This is the place where I should save only certain parameters of the voevent in the database
#         '''
#         alert.save()
        
        a = self.format_to_html(xml_filename)
                
        return a    

    
  
class Document(models.Model):
        
    docfile = models.FileField(upload_to='documents/')
    
        

   