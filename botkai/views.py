from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback
import os
import importlib

@csrf_exempt
def index(request):
    load_modules()
    result = "ok"
    try:
        body = json.loads(request.body)
        print(body, body.keys())
        if 'type' not in body.keys():
            result = "Неа."
        
        else:
            result = eval("callbackevents."+body["type"]+".index")
          





















        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)


def load_modules():
   files = os.listdir("callbackevents")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("callbackevents." + m[0:-3])