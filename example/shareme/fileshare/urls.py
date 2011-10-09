from django.conf.urls.defaults import patterns, url
from fileshare import handlers

urlpatterns = patterns('',
    url(r'^files$', handlers.NewFile(), name='new_file'),
    url(r'^files/(?P<id>\d+)$', handlers.GetFile(), name='get_file'),
)
