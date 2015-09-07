from django.shortcuts import render
from ..models import Group, Thread


def index(request):
    """
    Main index page
    """
    groups = Group.objects.order_by("name")[:12]
    threads = Thread.objects.order_by("-score", "-created")[:50]

    return render(request, "index.html", {
        "groups": groups,
        "threads": threads,
    })
