from django.conf.urls import url
from django.contrib import admin

from thiuff.shortcuts import flat_template
from threads.views import front, groups, threads
from threads import consumers
from users.views import auth, users
from chat import views as chat

urlpatterns = [
    url(r'^$', front.index),
    url(r'^about/$', flat_template("flat/about.html")),
    url(r'^contact/$', flat_template("flat/contact.html")),
    url(r'^coc/$', flat_template("flat/coc.html")),
    url(r'^privacy/$', flat_template("flat/privacy.html")),
    url(r'^auth/login/$', auth.login),
    url(r'^auth/logout/$', auth.logout),
    url(r'^auth/signup/$', auth.signup),
    url(r'^settings/$', users.settings),
    url(r'^chat/$', chat.index),
    url(r'^chat/post/$', chat.post),
    url(r'^u/([^/]+)/$', users.view),
    url(r'^g/$', groups.index),
    url(r'^g/create/$', groups.create),
    url(r'^g/([^/]+)/$', groups.view),
    url(r'^g/([^/]+)/edit/$', groups.edit),
    url(r'^g/([^/]+)/join/$', groups.join),
    url(r'^g/([^/]+)/leave/$', groups.leave),
    url(r'^g/([^/]+)/t/create/$', threads.create),
    url(r'^g/[^/]+/t/([^/]+)/$', threads.view),
    url(r'^g/[^/]+/t/([^/]+)/report/$', threads.report_thread),
    url(r'^g/[^/]+/t/([^/]+)/m/create/$', threads.create_top_level_message),
    url(r'^g/[^/]+/t/[^/]+/m/([^/]+)/edit/$', threads.edit_message),
    url(r'^g/[^/]+/t/[^/]+/m/([^/]+)/delete/$', threads.delete_message),
    url(r'^g/[^/]+/t/[^/]+/m/([^/]+)/reply/$', threads.create_reply_message),
    url(r'^g/[^/]+/t/[^/]+/m/([^/]+)/report/$', threads.report_message),
    url(r'^admin/', admin.site.urls),
]

channel_routing = {
    "websocket.connect": consumers.ws_connect,
    "websocket.keepalive": consumers.ws_keepalive,
    "websocket.receive": consumers.ws_message,
    "websocket.disconnect": consumers.ws_disconnect,
}
