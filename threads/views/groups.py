from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView

from ..forms.groups import CreateGroupForm
from ..models import Group


class CreateGroup(FormView):

    template_name = "groups/create.html"
    form_class = CreateGroupForm

    def form_valid(self, form):
        group = Group.objects.create(name=form.cleaned_data['name'])
        return redirect(group.urls.view)


def index(request):
    groups = Group.objects.filter()

    return render(
        request,
        "groups/index.html",
        {
            "groups": groups,
        },
    )


def view(request, group_name):
    try:
        group = Group.objects.get(name__iexact=group_name)
    except Group.DoesNotExist:
        raise Http404("No such group")
    threads = group.threads.order_by("-score", "-created")

    return render(
        request,
        "groups/view.html",
        {
            "group": group,
            "threads": threads,
        },
    )
