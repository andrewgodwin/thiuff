import functools
from django.http import Http404
from .models import User


def user_from_username(func):
    """
    Decorator which transforms a username into a user object.
    """
    @functools.wraps(func)
    def inner(request, username, *args, **kwargs):
        # Fetch the group
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise Http404("No such user")
        # Run the inner
        return func(request, user=user, *args, **kwargs)
    return inner
