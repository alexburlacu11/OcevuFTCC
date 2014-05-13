from django.conf.urls import patterns, include, url

from django.contrib import admin
from httplib import HTTPResponse
from django.http.response import HttpResponseRedirect

# from ztest.views import GenericView, AlertListView, AlertCreate, AlertDelete, AlertUpdate

from alertManager.views import AlertDetailView, AlertIndexView, AlertDeleteView, AlertCreateView, AlertUpdateView, AlertListView
from routineManager.views import RequestDetailView, RequestIndexView, RequestDeleteView, RequestCreateView, RequestUpdateView, RequestListView

from ztest.views import RequestWizard, RequestIndex
#  RequestIndex, RequestCreate, SequenceCreate,AlbumCreate,PlanCreate
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OcevuFTCC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#     url(r'^admin_tools/', include('admin_tools.urls')),
    
    url(r'^$', 'dashboard.views.index', name='index'),   
    url(r'^dashboard/login', 'dashboard.views.login_user', name='login_user'),
    url(r'^dashboard/logout', 'dashboard.views.logout_user', name='logout_user'),
    url(r'^dashboard/create', 'dashboard.views.create', name='create'),
    url(r'^dashboard/$', 'dashboard.views.main', name='main'),
    url(r'^dashboard/new_user', 'dashboard.views.new_user', name='new_user'),
    url(r'^dashboard/profile', 'dashboard.views.profile', name='profile'),
    url(r'^dashboard/update', 'dashboard.views.update', name='update'),
    
    url(r'^routinemanager2/$', RequestIndex.as_view() ),
#     url(r'^routinemanager2/create/', RequestCreate.as_view() ),
#     url(r'^routinemanager2/new_sequence/', SequenceCreate.as_view() ),
#     url(r'^routinemanager2/new_album/', AlbumCreate.as_view() ),
#     url(r'^routinemanager2/new_plan/', PlanCreate.as_view() ),
    url(r'^routinemanager2/wizard/', RequestWizard.as_view() ),
    url(r'^routinemanager2/edit/(?P<request_id>[-\d]+)$', RequestWizard.as_view() ),
    
    
#     url(r'^ztest/main', GenericView.as_view() ),
#     url(r'^ztest/insert', GenericView.as_view() ),
#     url(r'^ztest/alert/list/$', AlertListView.as_view() ),
#     url(r'^ztest/alert/add/$', AlertCreate.as_view(), name='alert_add'),
#     url(r'^ztest/alert/(?P<pk>\d+)/$', AlertUpdate.as_view(), name='alert_update'),
#     url(r'^ztest/alert/(?P<pk>\d+)/delete/$', AlertDelete.as_view(), name='alert_delete'),
    
    url(r'^guardian/', 'guardian.views.index', name='index'),
    url(r'^guardian/status', 'guardian.views.status', name='status'),
    url(r'^guardian/history', 'guardian.views.history', name='history'),
    
#     url(r'^routinemanager/main', 'routineManager.views.index', name='index'),
#     url(r'^routinemanager/add', 'routineManager.views.add', name='add'),
#     url(r'^routinemanager/delete', 'routineManager.views.delete', name='delete'),
#     url(r'^routinemanager/edit', 'routineManager.views.edit', name='edit'),
#     url(r'^routinemanager/list', 'routineManager.views.list', name='list'),
#     url(r'^routinemanager/view', 'routineManager.views.view', name='view'),
#     url(r'^routinemanager/loadfromfile', 'routineManager.views.loadfromfile', name='loadfromfile'),
#     url(r'^routinemanager/routine_request_to_db', 'routineManager.views.routine_request_to_db', name='routine_request_to_db'),
#     url(r'^routinemanager/update_to_db', 'routineManager.views.update_to_db', name='update_to_db'),
#     url(r'^routinemanager/upload_file', 'routineManager.views.upload_file', name='upload_file'),
    
    url(r'^alertmanager/$', AlertIndexView.as_view() ),
    url(r'^alertmanager/create', AlertCreateView.as_view() ),
    url(r'^alertmanager/delete/(?P<pk>\d+)/', AlertDeleteView.as_view() ),
    url(r'^alertmanager/update/(?P<pk>\d+)/', AlertUpdateView.as_view() ),
    url(r'^alertmanager/list', AlertListView.as_view() ),
    url(r'^alertmanager/view/(?P<pk>\d+)/', AlertDetailView.as_view() ),
    
    url(r'^routinemanager/$', RequestIndexView.as_view() ),
    url(r'^routinemanager/create', RequestCreateView.as_view() ),
    url(r'^routinemanager/delete/(?P<pk>\d+)/', RequestDeleteView.as_view() ),
    url(r'^routinemanager/update/(?P<pk>\d+)/', RequestUpdateView.as_view() ),
    url(r'^routinemanager/list', RequestListView.as_view() ),
    url(r'^routinemanager/view/(?P<pk>\d+)/', RequestDetailView.as_view() ),
    
#     url(r'^alertmanager/main', 'alertManager.views.index', name='index'),
#     url(r'^alertmanager/add', 'alertManager.views.add', name='add'),
#     url(r'^alertmanager/delete', 'alertManager.views.delete', name='delete'),
#     url(r'^alertmanager/edit', 'alertManager.views.edit', name='edit'),
#     url(r'^alertmanager/list', 'alertManager.views.list', name='list'),
#     url(r'^alertmanager/view', 'alertManager.views.view', name='view'),   
#     url(r'^alertmanager/loadfromfile', 'alertManager.views.loadfromfile', name='loadfromfile'),    
#     url(r'^alertmanager/alert_to_db', 'alertManager.views.alert_to_db', name='alert_to_db'),
#     url(r'^alertmanager/update_to_db', 'alertManager.views.update_to_db', name='update_to_db'),
#     url(r'^alertmanager/upload_file', 'alertManager.views.upload_file', name='upload_file'),
    

)
