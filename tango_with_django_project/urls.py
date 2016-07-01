from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from rango import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='rango/', permanent=False), name='index'), #remove from production
    url(r'^admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )