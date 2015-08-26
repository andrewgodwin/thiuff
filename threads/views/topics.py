from django.shortcuts import render, redirect

from ..forms.topics import CreateTopicForm
from ..models import Topic, Group


def create(request, group_name):
    """
    Creates a new Topic.
    """
    group = Group.objects.get(name=group_name)
    if request.method == "POST":
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.create(
                title=form.cleaned_data['title'],
                author=request.user,
                group=group,
            )
            return redirect(topic.urls.view)
    else:
        form = CreateTopicForm()
    return render(request, "topics/create.html", {
        "group": group,
        "form": form,
    })


def view(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render(request, "topics/view.html", {
        "group": topic.group,
        "topic": topic,
    })
