from django.contrib import auth
from django.shortcuts import render, redirect
from ..forms import LoginForm


def login(request):
    """
    Logs a user in.
    """
    # Form handling
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data["user"])
            return redirect("/")
    else:
        form = LoginForm()
    # Render
    return render(
        request,
        "auth/login.html",
        {"form": form},
    )


def logout(request):
    """
    Logs a user out.
    """
    auth.logout(request)
    return redirect("/")
