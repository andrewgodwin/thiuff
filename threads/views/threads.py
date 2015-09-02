import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

from thiuff.shortcuts import JsonResponse
from ..forms.threads import CreateThreadForm
from ..models import Thread, Message
from ..decorators import group_from_name, thread_from_id, message_from_id


@group_from_name
def create(request, group):
    """
    Creates a new Thread.
    """
    if request.method == "POST":
        form = CreateThreadForm(request.POST)
        if form.is_valid():
            thread = Thread.objects.create(
                title=form.cleaned_data['title'],
                url=form.cleaned_data.get('url', None),
                body=form.cleaned_data.get('body', None),
                author=request.user,
                group=group,
            )
            return redirect(thread.urls.view)
    else:
        form = CreateThreadForm()
    return render(request, "threads/create.html", {
        "group": group,
        "form": form,
    })


@thread_from_id
def view(request, thread):
    """
    Views a single thread page
    """

    return render(request, "threads/view.html", {
        "group": thread.group,
        "thread": thread,
    })


@thread_from_id
def create_top_level_message(request, thread):
    """
    Deals with creation of new top-level messages
    (called Discussions in site vocabulary)
    """
    if request.method == "POST":
        if request.POST.get("body"):
            message = Message.objects.create(
                thread=thread,
                author=request.user,
                body=request.POST['body']
            )
            return redirect(thread.urls.view)

    return render(request, "threads/create_top_level_message.html", {
        "thread": thread,
        "group": thread.group,
    })


@message_from_id
def edit_message(request, message):
    """
    Deals with creation of new top-level messages
    (called Discussions in site vocabulary)
    """
    if request.method == "POST":
        if request.POST.get("body"):
            message.body = request.POST['body']
            message.edited = datetime.datetime.utcnow()
            message.save()
            return redirect(message.thread.urls.view)

    return render(request, "threads/edit_message.html", {
        "thread": message.thread,
        "group": message.thread.group,
        "message": message,
    })


@message_from_id
def delete_message(request, message):
    """
    Deletes a message.
    """

    if request.method == "POST":
        if request.POST.get("delete"):
            message.deleted = datetime.datetime.utcnow()
            message.save()
        return redirect(message.thread.urls.view)

    return render(request, "threads/delete_message.html", {
        "thread": message.thread,
        "group": message.thread.group,
        "message": message,
    })


@message_from_id
def create_reply_message(request, parent):
    """
    Adds a reply to a thread.
    """
    if request.method == "POST":
        if request.POST.get("body"):
            message = Message.objects.create(
                thread=parent.thread,
                parent=parent,
                author=request.user,
                body=request.POST['body']
            )
            if request.is_ajax():
                return JsonResponse({
                    "id": str(message.id),
                })
            else:
                return redirect(message.thread.urls.view)

    return HttpResponse("Invalid method", status_code=405)
