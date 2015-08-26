from django.shortcuts import render
from ..models import User


def view(request, username):
    user = User.objects.get(username__iexact=username)

    return render(
        request,
        "users/view.html",
        {
            "user": user,
        },
    )
