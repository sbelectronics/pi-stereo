from django.shortcuts import render
from django.template import RequestContext, loader
import json

from stereocontroller import StereoPot, Power, Player

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
    Power.set_input( int(request.GET.get("value","2")))

    return HttpResponse("okey dokey")

def setFMStation(request):
    Player.set_station( request.GET.get("value","pandora") )

    return HttpResponse("okey dokey")

def setStation(request):
    Power.set_station( request.GET.get("value","q") )

    return HttpResponse("okey dokey")

def nextSong(request):
    if (Power.input == 3):
        # for FM, the <next> button is my commercial skip
        Power.delay_off(60)
    else:
       Power.next_song();

    return HttpResponse("okey dokey")

def loveSong(request):
    Power.love_song();

    return HttpResponse("okey dokey")

def banSong(request):
    Power.ban_song();

    return HttpResponse("okey dokey")

def getSettings(request):
    result = {}

    result["volumeSetPoint"] = StereoPot.setPoint
    result["volumeCurrent"] = StereoPot.value or 0
    result["volumeMoving"] = StereoPot.moving
    result["power"] = Power.power
    result["input"] = Power.input

    result["song"] = "unknown"
    result["artist"] = "unknown"
    result["station"] = "unknown"
    result["stationCount"] = "0"
    result["stations"] = []

    result["fmstation"] = Player.station

    try:
        lines = open("/home/pi/.config/pianobar/now_playing_vars").readlines()
        for line in lines:
            if (not "=" in line):
                continue
            (k,v) = line.split("=",1)

            if (k=="artist"):
                result["artist"] = v
            elif (k=="title"):
                result['song'] = v
            elif (k=="stationName"):
                result['station'] = v
            elif (k=="stationCount"):
                result['stationCount'] = v
            elif (k.startswith("station")):
                tmp = (k[7:], v)
                result["stations"].append(tmp)
    except:
        pass

    return HttpResponse(json.dumps(result), content_type='application/javascript')


