from django.conf.urls import patterns, include, url

from django.contrib import admin
from httplib import HTTPResponse
from django.http.response import HttpResponseRedirect

from ztest.views import GenericView, AlertListView, AlertCreate, AlertDelete, AlertUpdate
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OcevuFTCC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^ztest/main', GenericView.as_view() ),
    url(r'^ztest/insert', GenericView.as_view() ),
    url(r'^ztest/alert/list/$', AlertListView.as_view() ),
    url(r'^ztest/alert/add/$', AlertCreate.as_view(), name='alert_add'),
    url(r'^ztest/alert/(?P<pk>\d+)/$', AlertUpdate.as_view(), name='alert_update'),
    url(r'^ztest/alert/(?P<pk>\d+)/delete/$', AlertDelete.as_view(), name='alert_delete'),
    
    url(r'^guardian/', 'guardian.views.index', name='index'),
    url(r'^guardian/status', 'guardian.views.status', name='status'),
    url(r'^guardian/history', 'guardian.views.history', name='history'),
    
    url(r'^routinemanager/main', 'routineManager.views.index', name='index'),
    url(r'^routinemanager/add', 'routineManager.views.add', name='add'),
    url(r'^routinemanager/delete', 'routineManager.views.delete', name='delete'),
    url(r'^routinemanager/edit', 'routineManager.views.edit', name='edit'),
    url(r'^routinemanager/list', 'routineManager.views.list', name='list'),
    url(r'^routinemanager/view', 'routineManager.views.view', name='view'),
    url(r'^routinemanager/loadfromfile', 'routineManager.views.loadfromfile', name='loadfromfile'),
    url(r'^routinemanager/routine_request_to_db', 'routineManager.views.routine_request_to_db', name='routine_request_to_db'),
    url(r'^routinemanager/update_to_db', 'routineManager.views.update_to_db', name='update_to_db'),
    url(r'^routinemanager/upload_file', 'routineManager.views.upload_file', name='upload_file'),
    
    url(r'^alertmanager/main', 'alertManager.views.index', name='index'),
    url(r'^alertmanager/add', 'alertManager.views.add', name='add'),
    url(r'^alertmanager/delete', 'alertManager.views.delete', name='delete'),
    url(r'^alertmanager/edit', 'alertManager.views.edit', name='edit'),
    url(r'^alertmanager/list', 'alertManager.views.list', name='list'),
    url(r'^alertmanager/view', 'alertManager.views.view', name='view'),   
    url(r'^alertmanager/loadfromfile', 'alertManager.views.loadfromfile', name='loadfromfile'),    
    url(r'^alertmanager/alert_to_db', 'alertManager.views.alert_to_db', name='alert_to_db'),
    url(r'^alertmanager/update_to_db', 'alertManager.views.update_to_db', name='update_to_db'),
    url(r'^alertmanager/upload_file', 'alertManager.views.upload_file', name='upload_file'),
    
    url(r'^$', 'dashboard.views.index', name='index'),   
)
