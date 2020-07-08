from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback
import os
import importlib
from .events.confirmation import confirmation
from .events.message_new import message_new


events = {
    "confirmation" : confirmation,
    "message_new" : message_new,
    'message_reply' : message_new
}

def load_modules():
   files = os.listdir("botkai/events")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("botkai.events." + m[0:-3])


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
            result = events[body["type"]](request)






        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)



