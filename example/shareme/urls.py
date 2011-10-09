from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from simprest import docs

urlpatterns = patterns('',
    url(r'^$', docs, name='docs'),
    url(r'^v1/', include('fileshare.urls')),
)

if settings.SERVE_STATIC:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
