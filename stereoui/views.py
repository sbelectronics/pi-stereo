from django.shortcuts import render
from django.template import RequestContext, loader
import json

from stereocontroller import StereoPot, Power, Player, Mux

# Create your views here.

from django.http import HttpResponse

def index(request):
    template = loader.get_template('stereoui/index.html')
    context = RequestContext(request, {});
    return HttpResponse(template.render(context))

def setVolume(request):
    StereoPot.set( int(request.GET.get("volume","0")) )

    return HttpResponse("okey dokey")

def setPower(request):
    Power.set_power( request.GET.get("value","true")=="true" )

    return HttpResponse("okey dokey")

def setInput(request):
    #Power.set_input( int(request.GET.get("value","2")))
    Mux.set_channel( int(request.GET.get("value","0")) )

    return HttpResponse("okey dokey")

def setFMStation(request):
    Player.set_station( request.GET.get("value","pandora") )

    return HttpResponse("okey dokey")

def queueFile(request):
    Player.set_station( "file:" + request.GET.get("value",  "/home/pi/piano2.wav"),
                        artist = request.GET.get("artist", None),
                        song = request.GET.get("song", None),
                        immediate = False )

    return HttpResponse("okey dokey")

def setStation(request):
    Player.set_pandora_station( request.GET.get("value","q") )

    return HttpResponse("okey dokey")

def nextSong(request):
    if (Player.player=="fmradio"):   # was or (mux.input == 2)
        # for FM, the <next> button is my commercial skip
        Power.delay_off(60)
    else:
        Player.next_song();

    return HttpResponse("okey dokey")

def loveSong(request):
    Player.love_song();

    return HttpResponse("okey dokey")

def banSong(request):
    Player.ban_song();

    return HttpResponse("okey dokey")

def getSettings(request):
    result = {}

    result["volumeSetPoint"] = StereoPot.setPoint
    result["volumeCurrent"] = StereoPot.value or 0
    result["volumeMoving"] = StereoPot.moving
    result["power"] = Power.power
    result["input"] = Mux.input

    result["fmstation"] = Player.station

    result.update(Player.get_now_playing())

    return HttpResponse(json.dumps(result), content_type='application/javascript')


