from django.shortcuts import render
import json
import traceback

def index(request):
    try:
        print(json.loads(request.data))
        print((json.loads(request.data)).keys())
    except:
        print('Ошибка:\n', traceback.format_exc())
    return "ЩЛ"