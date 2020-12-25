from . import model_class
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib
from urllib.request import urlopen
import googlemaps
# Create your views here.

import tensorflow as tf
def hello(request):
    return HttpResponse('Hello World')

@csrf_exempt
def GeoLocating(request):
    result = None
    if request.method == 'POST':
        request_data = request.body
        print(request_data)
        request_dict = json.loads(request_data.decode('utf-8'))
        text = request_dict.get('sen')

        t = model_class(text)
        sen = ""
        vv = ""
        allPlace = ""
        interruptT = 0
        interruptV = 0
        interruptP = 0
        tt = ""
        for i in range(len(t[0])):
            tt = tt + t[0][i]
            if t[0][i] == 'T':
                if interruptT == i - 1:
                    interruptT = i
                    sen = sen + text[i]
                else:
                    sen = sen + " " + text[i]
                    interruptT = i
            if t[0][i] == 'V':
                if interruptV == i - 1:
                    interruptV = i
                    vv = vv + text[i]
                else:
                    vv = vv + " " + text[i]
                    interruptV = i
            if t[0][i] == 'P':
                if interruptP == i - 1:
                    interruptP = i
                    allPlace = allPlace + text[i]
                else:
                    allPlace = allPlace + " " + text[i]
                    interruptP = i


        result = {"initial": t, "targetPlace": sen, "places": allPlace,"verbs":vv}
    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")

@csrf_exempt
def CalculateLocating(request):
    result = None
    lat = None
    lng = None
    if request.method == 'POST':
        request_data = request.body
        print(request_data)
        request_dict = json.loads(request_data.decode('utf-8'))
        text = request_dict.get('location')
        address = urllib.parse.quote(text)
        url = 'http://api.geonames.org/searchJSON?q='+address+'&maxRows=1&username=logan1004'
        req = urlopen(url)
        res = req.read().decode()
        temp = json.loads(res)
        print(temp)
        lat = temp['geonames'][0]['lat']
        lng = temp['geonames'][0]['lng']

    result = {"latitude": lat, "longitude": lng}
    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")
