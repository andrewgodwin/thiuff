from django.http import Http404
from django.shortcuts import render, redirect

from ..forms.threads import CreateThreadForm
from ..models import Thread, Group


def create(request, group_name):
    """
    Creates a new Thread.
    """
    group = Group.objects.get(name=group_name)
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


def view(request, thread_id):
    """
    Views a single thread page
    """
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        raise Http404("No such thread")

    return render(request, "threads/view.html", {
        "group": thread.group,
        "thread": thread,
    })
