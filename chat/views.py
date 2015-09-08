import json
import channels
from django.shortcuts import render, redirect
from thiuff.shortcuts import JsonResponse


def index(request):
    """
    Shows the chat.
    """
    return render(request, "chat/index.html", {
    })


def post(request):
    """
    Receives a chat message.
    """
    if request.POST.get("message"):
        channels.Group("stream-chat").send({
            "content": json.dumps({
                "type": "chat",
                "message": request.POST["message"],
                "author": request.POST.get("author", "anonymous"),
            }),
        })
        return JsonResponse({"posted": True})
    return redirect("/chat/")
