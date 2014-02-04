from django.test import TestCase
from models import *
from django.db.models.sql.datastructures import DateTime
from array import array
# Create your tests here.

# datetime.date.today()


# class PollsViewsTestCase(TestCase):
#     def test_index(self):
#         resp = self.client.get('/polls/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue('latest_poll_list' in resp.context)
#         self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])
        
class WeatherWatcherTestCase(TestCase):
     def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)    
        print "basic addition success ! \n"
            
     def test_date_create(self):
        date = datetime.date.today()
        self.assertEqual(date, date)
        print "basic date test success ! \n"
        
     def test_db_access(self):
        aux_old = WeatherWatcher(
             port='/dev/ttyACM0', 
             date=datetime.date.today(), 
             sensor_value=0
        )
        aux_old.read_serial()
        aux_old.save()
        aux_new = WeatherWatcher.objects.first();
        aux_new.to_string()
        self.assertEqual(aux_new.sensor_value, aux_old.sensor_value)
        print "weather watcher db access success ! \n"
        
class SiteWatcherTestCase(TestCase):
     def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)    
        print "basic addition success ! \n"
            
     def test_date_create(self):
        date = datetime.date.today()
        self.assertEqual(date, date)
        print "basic date test success ! \n"
        
     def test_db_access(self):
        aux_old = SiteWatcher(
             port='/dev/ttyACM1', 
             date=datetime.date.today(), 
             sensor_value=0
        )
        aux_old.read_serial()
        aux_old.save()
        aux_new = SiteWatcher.objects.first();
        aux_new.to_string()
        self.assertEqual(aux_new.sensor_value, aux_old.sensor_value)
        print "site watcher db access success ! \n" 
        
class WatcherTestCase(TestCase):
      def test_polymorphism(self):
        print "polymorphism test: \n"
        w = WeatherWatcher(
             port='/dev/ttyACM0', 
             date=datetime.date.today(), 
             sensor_value=0
        )
        s = SiteWatcher(
             port='/dev/ttyACM1', 
             date=datetime.date.today(), 
             sensor_value=0
        )  
        ww = Watcher(
             port='/dev/ttyACM0', 
             date=datetime.date.today(), 
             sensor_value=0
        )
        watchers = [w,s]        
        
        for q in watchers:
            q.read_serial()
            q.save()
            
        for q in watchers:
            print "watcher says: \n"
            print q.to_string() 
      
    
    
    
    
    
     
        