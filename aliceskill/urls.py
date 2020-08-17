from django.urls import path


from .views import main

urlpatterns = [
    path("alice/", main),
]
