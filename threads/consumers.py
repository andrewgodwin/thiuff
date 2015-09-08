import json
from channels import Channel, Group
from channels.decorators import http_django_auth, channel_session
from .models import Group as GroupModel, Thread


@channel_session
def ws_connect(message):
    """
    Keeps websockets subscribed to channel Groups.
    """
    # Subscribe to the global site channel
    Group("global").add(message.reply_channel)
    # Keep streams subscribed
    for stream in message.channel_session.get("streams", []):
        Group("stream-%s" % stream).add(message.reply_channel)


@http_django_auth
@channel_session
def ws_message(message):
    # Parse incoming JSON message
    try:
        content = json.loads(message.content['content'])
        message_type = content['type']
    except ValueError:
        message.reply_channel.send(content=json.dumps({"error": "not-json"}))
    except KeyError:
        message.reply_channel.send(content=json.dumps({"error": "no-type"}))
    # Handle different types
    if message_type == "streams":
        # Add them to each stream's group
        for stream in content['streams']:
            try:
                allowed, reason = allow_stream(stream, message.user)
                # Allowed? Add them to the stream.
                if allowed:
                    Group("stream-%s" % stream).add(message.reply_channel)
                    message.channel_session['streams'] = message.channel_session.get("streams", []) + [stream]
                # Send the error reason back if denied
                else:
                    message.reply_channel.send(content=json.dumps({
                        "error": reason,
                        "stream": stream,
                    }))
            except:
                # Notify client of stream errors then reraise
                message.reply_channel.send(content=json.dumps({
                    "error": "stream-perm-internal-error",
                    "stream": stream,
                }))
                raise
    else:
        message.reply_channel.send(content=json.dumps({"error": "wrong-type"}))


def allow_stream(stream, user):
    """
    Logic that determines if user can subscribe to a stream.
    """
    # Chat is everyone
    if stream == "chat":
        return True, None
    # Threads are allowed if they can see the group
    elif stream.startswith("thread-"):
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


@channel_session
def ws_disconnect(message):
    """
    Removes websockets from subscribed channels as they disconnect.
    """
    Group("global").discard(message.reply_channel)
    for stream in message.channel_session.get("streams", []):
        Group("stream-%s" % stream).discard(message.reply_channel)
