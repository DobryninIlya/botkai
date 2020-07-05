from django.shortcuts import render

def index(request):
    print(request)
    return "ok"