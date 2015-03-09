from django.conf.urls import patterns, url

from stereoui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setVolume$', views.setVolume, name='setVolume'),
    url(r'^setPower$', views.setPower, name='setPower'),
    url(r'^getSettings$', views.getSettings, name='getSettings'),
)
