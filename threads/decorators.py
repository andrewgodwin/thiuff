import functools
from django.http import Http404
from .models import Thread, Group, Message


def group_from_name(func):
    """
    Decorator which transforms group name arguments into group objects
    """
    @functools.wraps(func)
    def inner(request, group_name, *args, **kwargs):
        # Fetch the group
        try:
            group = Group.objects.get(name__iexact=group_name)
        except Group.DoesNotExist:
            raise Http404("No such group")
        # Run the inner
        return func(request, group, *args, **kwargs)
    return inner


def thread_from_id(func):
    """
    Decorator which transforms thread ID arguments into thread objects
    """
    @functools.wraps(func)
    def inner(request, thread_id, *args, **kwargs):
        # Fetch the thread
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            raise Http404("No such thread")
        # Run the inner
        return func(request, thread, *args, **kwargs)
    return inner


def message_from_id(func):
    """
    Decorator which transforms message ID arguments into message objects
    """
    @functools.wraps(func)
    def inner(request, message_id, *args, **kwargs):
        # Fetch the message
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            raise Http404("No such message")
        # Run the inner
        return func(request, message, *args, **kwargs)
    return inner
