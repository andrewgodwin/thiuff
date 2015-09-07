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


class ChangePasswordForm(forms.Form):
    """
    Password change form
    """

    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_again = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        op = self.cleaned_data['old_password']
        if not self.user.check_password(op):
            raise forms.ValidationError("Old password is incorrect.")

    def clean_new_password_again(self):
        npa = self.cleaned_data['new_password_again']
        np = self.cleaned_data.get("new_password", None)
        if np and npa != np:
            raise forms.ValidationError("New passwords did not match.")
        return npa
