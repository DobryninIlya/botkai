from django.shortcuts import render
import json
import traceback

def index(request):
    try:
        print(request.body)
    except:
        print('Ошибка:\n', traceback.format_exc())
    return "ЩЛ"