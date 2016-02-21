from django.conf.urls import patterns, url

from stereoui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setVolume$', views.setVolume, name='setVolume'),
    url(r'^setPower$', views.setPower, name='setPower'),
    url(r'^setInput$', views.setInput, name='setInput'),
    url(r'^setFMStation$', views.setFMStation, name='setFMStation'),
    url(r'^setStation$', views.setStation, name='setStation'),
    url(r'^nextSong$', views.nextSong, name='nextSong'),
    url(r'^banSong$', views.banSong, name='banSong'),
    url(r'^loveSong$', views.loveSong, name='loveSong'),
    url(r'^getSettings$', views.getSettings, name='getSettings'),
)
