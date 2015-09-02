from channels import Channel, Group
from channels.decorators import consumer, http_django_auth

@consumer("django.websocket.connect", "django.websocket.keepalive")
@http_django_auth
def ws_add(channel, send_channel, user, **kwargs):
    pass

@consumer("django.websocket.receive")
@http_django_auth
def ws_message(channel, send_channel, content, user, **kwargs):
    if content.startswith("streams "):
        streams = content[8:].split()
        print "User %s trying to listen to streams %s" % (user, streams)
    else:
        Channel(send_channel).send(content="error")

@consumer("django.websocket.disconnect")
@http_django_auth
def ws_disconnect(channel, send_channel, user, **kwargs):
    pass
