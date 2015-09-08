import json
from django.shortcuts import render
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    """
    Custom response class that encodes the content to JSON.
    """

    def __init__(self, content):
        super(JsonResponse, self).__init__(
            json.dumps(content),
            content_type="application/json",
        )


def flash(request, message, type="info"):
    """
    Add a message to be shown on the next page load.
    """
    request.session['messages'] = request.session.get("messages", []) + [(type, message)]


def get_flashes(request):
    """
    Gets any pending flashes and clears the pending set.
    """
    messages = request.session.get("messages", [])
    if messages:
        del request.session["messages"]
    return messages


def flat_template(template_name):
    """
    A view that renders a flat template.
    """
    def view(request):
        return render(request, template_name)
    return view
