from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from . import views

urlpatterns = patterns('',
    url(r'^djangotest$', views.djangotest),
    url(r'^usermanual$', views.usermanual),
    url(r'^modeltest$', views.modeltest),
    url(r'^search$', views.search),
    url(r'^ResultPage.html$', views.result),
)
