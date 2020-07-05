from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback

@csrf_exempt
def index(request):
    try:
        print(request.body)
        print(request.method)
        print(request.META)
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse("ok")