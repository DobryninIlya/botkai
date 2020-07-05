from django.shortcuts import render
import json

def index(request):
    print(json.loads(request.data))
    print((json.loads(request.data)).keys())
    return "ЩЛ"