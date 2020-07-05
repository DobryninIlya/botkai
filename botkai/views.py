from django.shortcuts import render

def index(request):
    print(request.data)
    return "ok"