from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^search$', views.search),
    url(r'^ResultPage.html$', views.result),
    url(r'^DetailPage.html$', views.detail),
)
