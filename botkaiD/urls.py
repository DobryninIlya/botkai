"""botkaiD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.views.static import serve
from botkai.views import index, web_yandex, miniapp, index, main_miniapp, download_ics


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^botkai/', include("botkai.urls")),
    url(r'^botkai/miniapp/$', miniapp),
    url(r'^botkai/miniapp/main/$', main_miniapp),

    url('botkai/', index),
    path('yandex_f66897e4739fe69c.html', web_yandex),
    path('assistent/', include("aliceskill.urls")),

    url('download/', download_ics),  # {'path': "./bot.db"}),

url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
