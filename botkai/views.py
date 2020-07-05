from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import traceback

@csrf_exempt
def index(request):
    result = "ok"
    try:
        body = json.loads(request.body)
        print(body, body.keys())
          





















        
    except:
        print('Ошибка:\n', traceback.format_exc())
    return HttpResponse(result)