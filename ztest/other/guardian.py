
from guardian.models import *
from threading import Thread
from time import sleep


# this script will permanently read the database values for the weather, 
# site and environment watchers and decide whether it is ok to make
# an observation. The table which it inserts data into is 
# "guardian". It has a general loop inside which it reads data and
# decides accordingly

def loop():

    GOOD = True
    BAD = False 
    
 

    while(True):
        #initialise the watchers
        now = datetime.datetime.now()
        weather = WeatherWatcher(
             port='/dev/ttyACM0', 
             date=now, 
             sensor_value=0
        )
        site = SiteWatcher(
             port='/dev/ttyACM1', 
             date=now, 
             sensor_value=0
        )  
        
        security = SecurityWatcher(
             port='/dev/ttyACM1', 
             date=now, 
             sensor_value=0
        )
        
        watchers = [weather, site, security] 
                       
               
        for watcher in watchers:
            watcher.set_date(now)
            watcher.read_serial()            
            watcher.save()
            print watcher.to_string
        
        #the initial weather is good
        choice_weather = GOOD
        choice_site = GOOD
        choice_security = GOOD
        
        #check sensor_value, if it is out of range, there is a problem
        if (int(watchers[0].sensor_value) > 1000 ):
            choice_weather = BAD
        
        if (int(watchers[1].sensor_value) > 1000 ):
            choice_site = BAD
            
        if (int(watchers[2].sensor_value) > 1000 ):
            choice_security = BAD
        
        guardian = Guardian(
                date = now,
                weather_flag = choice_weather,
                site_flag = choice_site,
                security_flag = choice_security            
        )
        guardian.save()
        print guardian.to_string()      
        print "\n" 
        
        
        sleep(5)    
          #to do : optimize, check CPU performance


if  __name__ =='__main__':
    thread = Thread(target = loop)
    thread.start()
    #thread.join()
    print "thread finished...exiting"