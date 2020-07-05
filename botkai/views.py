from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback
import os
import importlib

from .callbackevents.confirmation import func

def load_modules():
   files = os.listdir(".callbackevents")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module(r".callbackevents." + m[0:-3])
       

#load_modules()

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
            func()





















        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)



