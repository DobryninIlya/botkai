from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback
import os
import importlib

from .events.confirmation import confirmation
from .events.message_new import message_new
from .events.vkpay_transaction import vkpay_transaction
from .events.group_leave import group_leave
from .events.group_join import group_join

from pprint import pprint

events = {
    "confirmation" : confirmation,
    "message_new" : message_new,
    "message_event" : message_new,
    "vkpay_transaction" : vkpay_transaction,
    "group_leave" : group_leave,
    "group_join" : group_join,
   
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
        pprint(body)
        if 'type' not in body.keys():
            result = "Неа."
        
        else:
            result = events[body["type"]](request)






        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)


def miniapp(request):
    return render(request, 'botkaiapp/index.html')


def web_yandex(request):
    return render(request, 'botkaiapp/yandex_f66897e4739fe69c.html')

