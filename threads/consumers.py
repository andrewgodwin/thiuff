import json
from channels import Channel, Group
from channels.decorators import http_django_auth, send_channel_session


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
def ws_message(channel, send_channel, content, user, session, channel_session, **kwargs):
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
            # Threads are public right now, so no need to do checks.
            if stream.startswith("thread-"):
                pass
            # Only allow the same user into a user stream
            elif stream.startswith("user-"):
                if stream[5:] != str(user.id):
                    Channel(send_channel).send(content=json.dumps({
                        "error": "not-allowed-stream",
                        "stream": stream,
                    }))
                    continue
            # Deny unknown streams
            else:
                Channel(send_channel).send(content=json.dumps({
                    "error": "unknown-stream",
                    "stream": stream,
                }))
                continue
            # Got this far? Add them to the stream.
            Group("stream-%s" % stream).add(send_channel)
            channel_session['streams'] = channel_session.get("streams", []) + [stream]
    else:
        Channel(send_channel).send(content="error")


@send_channel_session
def ws_disconnect(channel, send_channel, channel_session, **kwargs):
    """
    Removes websockets from subscribed channels as they disconnect.
    """
    Group("global").discard(send_channel)
    for stream in getattr(channel_session, "streams", []):
        Group("stream-%s" % stream).discard(send_channel)
