from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import importlib
import os
from .events.confirmation import confirmation
from .events.message_new import message_new
from .events.vkpay_transaction import vkpay_transaction
from .events.group_leave import group_leave
from .events.group_join import group_join
from botkai.fileserver.make_ics_response import main as make_ics_response

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

        if 'type' not in body.keys():
            result = "Неа."
        
        else:
            result = events[body["type"]](request)






    except SystemExit:
        # print("ВЫХОД")
        quit(1)
        # os.system("echo EXITING APP")
        # os.system("touch reload.py")
        # os.system("pkill gunicorn")
        # os.system("gunicorn botkaiD.wsgi --log-file -")
    except:
        #print('Ошибка:\n', traceback.format_exc())
        result = "Почти получилось :)"
    return HttpResponse(result)


def miniapp(request):
    return render(request, 'botkaiapp/index.html')


def main_miniapp(request):
    return render(request, 'botkaiapp/main.html')


def web_yandex(request):
    return render(request, 'botkaiapp/yandex_f66897e4739fe69c.html')

import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseForbidden

def download_ics(request):
    file = make_ics_response(request.GET.get("groupid", ""))
    if not request.GET.get("groupid", ""):
        raise Http404
    if not file:
        raise Http404
    path = "./{}".format(file)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404