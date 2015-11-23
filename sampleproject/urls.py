from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.conf import settings as mysettings 

urlpatterns = patterns('',
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': mysettings.MEDIA_ROOT}),
    url(r'^/?$', 'home.views.home', name='site_home'),
    url(r'^articles/', include('articles.urls')),
)
