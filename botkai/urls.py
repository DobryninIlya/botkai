from django.urls import path

from .views import index
from .views import miniapp
from .distribution import main as distribution

urlpatterns = [
    # path("", index),
    # path(r'^miniapp/$', miniapp),
    # path("distribution/", distribution),
]
