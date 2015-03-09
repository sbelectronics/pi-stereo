from django.shortcuts import render
from django.template import RequestContext, loader
import json

from stereopot import StereoPot

# Create your views here.

from django.http import HttpResponse

def index(request):
    template = loader.get_template('stereoui/index.html')
    context = RequestContext(request, {});
    return HttpResponse(template.render(context))

def setVolume(request):
    StereoPot.set( int(request.GET.get("power","0")) )

    return HttpResponse("okey dokey")

def setPower(request):
    # do it

    # request.GET.get("value","true")=="true", ,

    return HttpResponse("okey dokey")

def getSettings(request):
    result = {}

    result["volumeSetPoint"] = StereoPot.setPoint
    result["volumeCurrent"] = StereoPot.value

    return HttpResponse(json.dumps(result), content_type='application/javascript')


