"""thiuff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
from django.contrib import admin

from threads.views import front, groups, topics
from users.views import auth

urlpatterns = [
    url(r'^$', front.index),
    url(r'^auth/login/$', auth.login),
    url(r'^auth/logout/$', auth.logout),
    url(r'^g/create/$', groups.CreateGroup.as_view()),
    url(r'^g/([^/]+)/$', groups.view),
    url(r'^g/([^/]+)/t/create/$', topics.create),
    url(r'^g/[^/]+/t/([^/]+)/$', topics.view),
    url(r'^admin/', admin.site.urls),
]
