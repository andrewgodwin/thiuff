import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from thiuff.shortcuts import JsonResponse, flash
from ..forms.threads import CreateThreadForm, ReportForm
from ..models import Thread, Message, Report
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


@login_required
@thread_from_id
def report_thread(request, thread):
    """
    Makes a report for a thread.
    """

    # Cancel button support
    if request.POST.get("cancel"):
        return redirect(thread.urls.view)

    # Form processing
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                thread=thread,
                type=form.cleaned_data['type'],
                comment=form.cleaned_data['comment'],
                reporter=request.user,
                accused=thread.author,
            )
            flash(request, "Report submitted. Thanks!")
        return redirect(thread.urls.view)
    else:
        form = ReportForm()

    return render(request, "threads/report.html", {
        "form": form,
        "report_url": thread.urls.report,
    })


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
@message_from_id
def report_message(request, message):
    """
    Makes a report for a message.
    """

    # Cancel button support
    if request.POST.get("cancel"):
        return redirect(message.thread.urls.view)

    # Form processing
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                message=message,
                type=form.cleaned_data['type'],
                comment=form.cleaned_data['comment'],
                reporter=request.user,
                accused=message.author,
            )
            flash(request, "Report submitted. Thanks!")
        return redirect(message.thread.urls.view)
    else:
        form = ReportForm()

    return render(request, "threads/report.html", {
        "form": form,
        "report_url": message.urls.report,
    })
