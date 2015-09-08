from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from thiuff.shortcuts import flash

from ..forms.groups import CreateGroupForm, EditGroupForm
from ..models import Group, GroupMember
from ..decorators import group_from_name, object_permission


def index(request):
    your_groups = []
    if request.user.is_authenticated():
        your_groups = [x.group for x in request.user.memberships.select_related("group")]
        your_groups.sort(key=lambda g: g.name)
    all_groups = Group.objects.order_by("-num_members")

    return render(request, "groups/index.html", {
        "all_groups": all_groups,
        "your_groups": your_groups,
    })


@group_from_name
@object_permission("group", "view")
def view(request, group):
    """
    Shows a group front page
    """
    threads = group.threads.order_by("-score", "-created")
    return render(request, "groups/view.html", {
        "group": group,
        "threads": threads,
    })


@login_required
def create(request):
    """
    Makes a new group
    """
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = Group.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
            )
            return redirect(group.urls.view)
    else:
        form = CreateGroupForm()
    return render(request, "groups/create.html", {
        "form": form,
    })


@login_required
@group_from_name
@object_permission("group", "edit")
def edit(request, group):
    """
    Edits group settings
    """
    if request.method == "POST":
        form = EditGroupForm(request.POST)
        if form.is_valid():
            group.description = form.cleaned_data['description']
            group.colour = form.cleaned_data['colour']
            group.save()
            flash(request, "Settings saved.")
            return redirect(group.urls.edit)
    else:
        form = EditGroupForm(initial={
            "description": group.description,
            "colour": group.colour,
        })
    return render(request, "groups/edit.html", {
        "group": group,
        "form": form,
    })


@login_required
@group_from_name
def join(request, group):
    """
    Joins a group (optionally prompting for more info)
    """
    # TODO: make all joins POST with CSRF
    # No more info form for now, and no pending statuses
    membership = group.membership(request.user)
    if membership is None:
        GroupMember.objects.create(
            group=group,
            user=request.user,
            status="member",
        )
        flash(request, "You are now a member of the group!")

    return redirect(group.urls.view)


@login_required
@group_from_name
def leave(request, group):
    """
    Leaves a group (optionally prompting for confirmation if getting back
    into the group is not trivial)
    """
    # TODO: make all leaves POST with CSRF
    # Just protect against the last admin leaving for now.
    membership = group.membership(request.user)
    if membership is None or membership.status == "banned":
        return redirect(group.urls.view)

    if membership.status == "admin":
        if group.members.filter(status="admin").count() == 1:
            return render(request, "groups/leave_error.html", {
                "group": group,
                "reason": "you are the last admin",
            })

    membership.delete()
    flash(request, "You are no longer a member of the group.")

    return redirect(group.urls.view)
