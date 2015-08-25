from django.shortcuts import render


def index(request):
    """
    Main index page
    """

    return render(request, "index.html", {})
