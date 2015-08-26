from django import forms
from django.contrib.auth import authenticate
from .models import User


class LoginForm(forms.Form):
    """
    Login form
    """

    username = forms.CharField(label="Username/Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        # Try getting by username first
        user = User.by_username(username)
        # Then by email
        if user is None and "@" in username:
            user = User.by_identifier("email", username)
            if user is None:
                raise forms.ValidationError("There is no user account with that username or email address.")
        elif user is None:
            raise forms.ValidationError("There is no user account with that username.")
        # Check if deactivated
        if not user.is_active:
            raise forms.ValidationError("Your user account has been deactivated.")
        # Stick user into cleaned data
        self.cleaned_data["user"] = user
        return username

    def clean_password(self):
        # Bail if there's no user
        user = self.cleaned_data.get("user", None)
        if user is None:
            return None
        # Re-fetch user using authenticate
        self.cleaned_data["user"] = authenticate(username=user.username, password=self.cleaned_data['password'])
        if self.cleaned_data["user"] is None:
            raise forms.ValidationError("Incorrect password.")
        return None
