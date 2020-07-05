from django.shortcuts import render
from django.http import HttpResponse
import json
import traceback


def index(request):
    try:
        pass
        #print(request.body)
        #print(request.method)
        #print(request.META)
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse("ok")