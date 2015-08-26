import json

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
