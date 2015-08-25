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


def view(request, group_name):
    group = Group.objects.get(name__iexact=group_name)
    return render(
        request,
        "groups/view.html",
        {
            "group": group,
        },
    )
