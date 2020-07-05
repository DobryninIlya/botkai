from django.shortcuts import render
import json
import traceback

def index(request):
    try:
        print(json.loads(request.body))
        print((json.loads(request.body)).keys())
    except:
        print('Ошибка:\n', traceback.format_exc())
    return "ЩЛ"