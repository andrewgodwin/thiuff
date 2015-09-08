import json
from channels import Channel, Group
from channels.decorators import http_django_auth, send_channel_session
from .models import Group as GroupModel, Thread


@send_channel_session
def ws_connect(channel, send_channel, channel_session, **kwargs):
    """
    Keeps websockets subscribed to channel Groups.
    """
    # Subscribe to the global site channel
    Group("global").add(send_channel)
    # Keep streams subscribed
    for stream in channel_session.get("streams", []):
        Group("stream-%s" % stream).add(send_channel)


@http_django_auth
@send_channel_session
def ws_message(channel, send_channel, content, user, channel_session, **kwargs):
    # Parse incoming JSON message
    try:
        content = json.loads(content)
        message_type = content['type']
    except ValueError:
        Channel(send_channel).send(content=json.dumps({"error": "not-json"}))
    except KeyError:
        Channel(send_channel).send(content=json.dumps({"error": "no-type"}))
    # Handle different types
    if message_type == "streams":
        # Add them to each stream's group
        for stream in content['streams']:
            try:
                allowed, reason = allow_stream(stream, user)
                # Allowed? Add them to the stream.
                if allowed:
                    Group("stream-%s" % stream).add(send_channel)
                    channel_session['streams'] = channel_session.get("streams", []) + [stream]
                # Send the error reason back if denied
                else:
                    Channel(send_channel).send(content=json.dumps({
                        "error": reason,
                        "stream": stream,
                    }))
            except:
                # Notify client of stream errors then reraise
                Channel(send_channel).send(content=json.dumps({
                    "error": "stream-perm-internal-error",
                    "stream": stream,
                }))
                raise
    else:
        Channel(send_channel).send(content=json.dumps({"error": "wrong-type"}))


def allow_stream(stream, user):
    """
    Logic that determines if user can subscribe to a stream.
    """
    # Threads are allowed if they can see the group
    if stream.startswith("thread-"):
        thread = Thread.objects.get(id=stream[7:])
        return thread.group.has_permission(user, "view"), "stream-denied"
    # Groups are allowed if they can see the group
    elif stream.startswith("group-"):
        group = GroupModel.objects.get(id=stream[6:])
        return group.has_permission(user, "view"), "stream-denied"
    # Only allow the same user into a user stream
    elif stream.startswith("user-"):
        return stream[5:] == str(user.id), "stream-denied"
    # Deny unknown streams
    else:
        return False, "stream-unknown"


@send_channel_session
def ws_disconnect(channel, send_channel, channel_session, **kwargs):
    """
    Removes websockets from subscribed channels as they disconnect.
    """
    Group("global").discard(send_channel)
    for stream in getattr(channel_session, "streams", []):
        Group("stream-%s" % stream).discard(send_channel)
