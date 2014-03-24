from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OcevuFTCC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'test.views.test', name='test'),
    url(r'^guardian/', 'guardian.views.index', name='index'),
    url(r'^guardian/status', 'guardian.views.status', name='status'),
    url(r'^guardian/history', 'guardian.views.history', name='history'),
    url(r'^voeventvisualizer/$', 'alertManager.views.index', name='index'),
    
                       
)
