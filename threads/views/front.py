from django.shortcuts import render
from ..models import Group, Thread


def index(request):
    """
    Main index page
    """
    groups = Group.objects.filter(frontpage=True).order_by("name")[:12]
    threads = Thread.objects.filter(group__frontpage=True).order_by("-score", "-created")[:50]

    return render(request, "index.html", {
        "groups": groups,
        "threads": threads,
    })
