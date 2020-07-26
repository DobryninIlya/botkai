from django.urls import path

from .views import index
from .views import miniapp

urlpatterns = [
    path("", index),
    path("miniapp/", miniapp),
]
