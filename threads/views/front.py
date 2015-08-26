from django.shortcuts import render
from ..models import Group


def index(request):
    """
    Main index page
    """

    groups = Group.objects.order_by("name")[:12]

    return render(request, "index.html", {
        "groups": groups,
    })
