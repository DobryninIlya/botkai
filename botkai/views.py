from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback
import os
import importlib

from .events.confirmation import func

def load_modules():
   files = os.listdir("/app/botkai/events")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module(".events." + m[0:-3] + ".func")


load_modules()

@csrf_exempt
def index(request):

    result = "ok"
    try:
        body = json.loads(request.body)
        print(body, body.keys())
        if 'type' not in body.keys():
            result = "Неа."
        
        else:
            #result = eval(body["type"]+".index")
            #result = eval("/callbackevents/confirmation.index")
            print(os.path.abspath(__file__))
            result = func()





















        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)



