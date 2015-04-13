from http.client import HTTPResponse

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.views.generic.base import RedirectView

from alertManager.views import AlertDetailView, AlertIndexView, AlertDeleteView, AlertCreateView, AlertUpdateView, AlertListView


# from ztest.views import GenericView, AlertListView, AlertCreate, AlertDelete, AlertUpdate
#  RequestIndex, RequestCreate, SequenceCreate,AlbumCreate,PlanCreate
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fgft_cc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#     url(r'^admin_tools/', include('admin_tools.urls')),
    
    url(r'^$', 'ismn.views.index', name='index'),   
    url(r'^ismn/login', 'ismn.views.login_user', name='login_user'),
    url(r'^ismn/logout', 'ismn.views.logout_user', name='logout_user'),
    url(r'^ismn/create', 'ismn.views.create', name='create'),
    url(r'^ismn/$', 'ismn.views.main', name='main'),
    url(r'^ismn/new_user', 'ismn.views.new_user', name='new_user'),
    url(r'^ismn/profile', 'ismn.views.profile', name='profile'),
#     url(r'^ismn/update', 'ismn.views.update', name='update'),
    
#     url(r'^routinemanager2/$', RequestIndex.as_view() ),
#     url(r'^routinemanager2/create/', RequestCreate.as_view() ),
#     url(r'^routinemanager2/new_sequence/', SequenceCreate.as_view() ),
#     url(r'^routinemanager2/new_album/', AlbumCreate.as_view() ),
#     url(r'^routinemanager2/new_plan/', PlanCreate.as_view() ),
#     url(r'^routinemanager2/wizard/', RequestWizard.as_view() ),
#     url(r'^routinemanager2/edit/(?P<request_id>[-\d]+)$', RequestWizard.as_view() ),
    
    url(r'^routinemanager/$', 'routineManager.views.index', name='index'),
    url(r'^routinemanager/request_create', 'routineManager.views.request_create', name='request_create'),
    url(r'^routinemanager/request_save', 'routineManager.views.request_save', name='request_save'),
    url(r'^routinemanager/sequence_save', 'routineManager.views.sequence_save', name='sequence_save'),
    url(r'^routinemanager/album_save', 'routineManager.views.album_save', name='album_save'),
    url(r'^routinemanager/plan_save', 'routineManager.views.plan_save', name='plan_save'),
    url(r'^routinemanager/edit_request/(?P<slug>\d+)', 'routineManager.views.edit_request', name='edit_request'),
    url(r'^routinemanager/edit_sequence/(?P<slug>\d+)', 'routineManager.views.edit_sequence', name='edit_sequence'),
    url(r'^routinemanager/edit_album/(?P<slug>\d+)', 'routineManager.views.edit_album', name='edit_album'),
    url(r'^routinemanager/edit_plan/(?P<slug>\d+)', 'routineManager.views.edit_plan', name='edit_plan'),
    url(r'^routinemanager/help_request/', 'routineManager.views.help_request', name='help_request'),
    url(r'^routinemanager/help_sequence/', 'routineManager.views.help_sequence', name='help_sequence'),
    url(r'^routinemanager/help_album/', 'routineManager.views.help_album', name='help_album'),
    url(r'^routinemanager/help_plan/', 'routineManager.views.help_plan', name='help_plan'),     
    url(r'^routinemanager/getjd1jd2/$', 'routineManager.views.getJd1Jd2', name='getJd1Jd2'),    
#     url(r'^ztest/main', GenericView.as_view() ),
#     url(r'^ztest/insert', GenericView.as_view() ),
#     url(r'^ztest/alert/list/$', AlertListView.as_view() ),
#     url(r'^ztest/alert/add/$', AlertCreate.as_view(), name='alert_add'),
#     url(r'^ztest/alert/(?P<pk>\d+)/$', AlertUpdate.as_view(), name='alert_update'),
#     url(r'^ztest/alert/(?P<pk>\d+)/delete/$', AlertDelete.as_view(), name='alert_delete'),
    
    url(r'^monitoring/', 'monitoring.views.index', name='index'),
#     url(r'^monitoring/status', 'monitoring.views.status', name='status'),
#     url(r'^monitoring/history', 'monitoring.views.history', name='history'),
    
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
    
#     url(r'^routinemanager/$', RequestIndexView.as_view() ),
#     url(r'^routinemanager/create', RequestCreateView.as_view() ),
#     url(r'^routinemanager/delete/(?P<pk>\d+)/', RequestDeleteView.as_view() ),
#     url(r'^routinemanager/update/(?P<pk>\d+)/', RequestUpdateView.as_view() ),
#     url(r'^routinemanager/list', RequestListView.as_view() ),
#     url(r'^routinemanager/view/(?P<pk>\d+)/', RequestDetailView.as_view() ),
    
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

    url(r'^planner/$', 'planner.views.index', name='index'),  
    url(r'^planner/current_planning/$', 'planner.views.viewCurrentPlanning', name='viewCurrentPlanning'),  
    url(r'^planner/older_plannings/list/$', 'planner.views.getOlderPlannings', name='getOlderPlannings'),  
    url(r'^planner/older_plannings/view/(?P<idPlan>\d+)/', 'planner.views.viewOlderPlanning', name='viewOlderPlanning'), 
    
    url(r'^dashboard/$', 'ismn.views.dashboard', name='dashboard'),    
    url(r'^voevent_viewer/$', 'ismn.views.voevent_viewer', name='voevent_viewer'),  
   

)
