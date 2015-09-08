from django.contrib import auth
from django.shortcuts import render, redirect
from ..forms import LoginForm, SignupForm
from ..models import UserAuth, User


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


def signup(request):
    """
    Makes a new user.
    """
    # Form handling
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Make user
            user = User.objects.create(
                username=form.cleaned_data['username'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Make email identifier link
            UserAuth.objects.create(
                user=user,
                type="email",
                identifier=form.cleaned_data['email'],
            )
            # Log them in (need to run through authenticate to get one
            # we can pass to login with the auth backend on it)
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            auth.login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
    # Render
    return render(
        request,
        "auth/signup.html",
        {"form": form},
    )
