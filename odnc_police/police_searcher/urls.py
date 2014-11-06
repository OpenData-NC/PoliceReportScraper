from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_skeleton2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
  #  url(r'^130.211.132.6/home$', views.search),
   # url(r'^130.211.132.6/search$', views.result),
   # url(r'^130.211.132.6/result$', views.detail),
    url(r'^djangotest$', views.djangotest),
)

