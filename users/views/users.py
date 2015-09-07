from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from thiuff.shortcuts import flash
from ..models import User
from ..decorators import user_from_username
from ..forms import ChangePasswordForm


@user_from_username
def view(request, user):
    return render(request, "users/view.html", {
        "profile_user": user,
    })


@login_required
def settings(request):
    """
    The user's own settings
    """
    user = request.user

    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            flash(request, "Password changed!")
            return redirect(".")
    else:
        form = ChangePasswordForm(user)

    return render(request, "users/settings.html", {
        "form": form,
    })
