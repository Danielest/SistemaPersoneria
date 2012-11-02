from django.conf.urls import patterns,url
from docs import views

urlpatterns = patterns('',
    #paginas para informes
    url(r'^$', views.index, name='index'),

    #paginas para ciudadanos
    url(r'^ciudadano/?$', views.indexCiudadano, name='indexCiudadano'),
    url(r'^ciudadano/(?P<ciud_id>\d+)/$', views.singleCiudadano, name='singleCiudadano'),

    #paginas para tutelas
    url(r'^tutela/?$', views.indexTutela, name='indexTutela'),
    url(r'^tutela/(?P<tut_id>\d+)/$', views.singleTutela, name='singleTutela'),

    url(r'^pdf/', views.pruebapdf, name='pdf'),

)

