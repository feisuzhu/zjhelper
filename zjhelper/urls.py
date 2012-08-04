from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from salary import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zjhelper.views.home', name='home'),
    # url(r'^zjhelper/', include('zjhelper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.index),
    url(r'^reports$', views.reports),
    url(r'^autofill$', views.autofill),
    url(r'^admin/', include(admin.site.urls)),
)
