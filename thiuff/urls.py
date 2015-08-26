from django.conf.urls import url
from django.contrib import admin

from threads.views import front, groups, threads
from users.views import auth, users

urlpatterns = [
    url(r'^$', front.index),
    url(r'^auth/login/$', auth.login),
    url(r'^auth/logout/$', auth.logout),
    url(r'^u/([^/]+)/$', users.view),
    url(r'^g/$', groups.index),
    url(r'^g/create/$', groups.CreateGroup.as_view()),
    url(r'^g/([^/]+)/$', groups.view),
    url(r'^g/([^/]+)/t/create/$', threads.create),
    url(r'^g/[^/]+/t/([^/]+)/$', threads.view),
    url(r'^admin/', admin.site.urls),
]
