from django.conf.urls import patterns, include, url

from django.views.static import * 
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'personeria.views.home', name='home'),
    # url(r'^personeria/', include('personeria.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^docs/',include('docs.urls',namespace="docs")),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/',include(admin.site.urls)),
    #para las rutas estaticas
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
