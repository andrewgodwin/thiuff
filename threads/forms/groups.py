import re
from django import forms
from django.conf import settings
from ..models import Group


class CreateGroupForm(forms.Form):

    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        # Check characters
        if not re.match(r"[a-z0-9\-\_]", name):
            raise forms.ValidationError("Invalid characters in name; use only a-z, digits, underscores and hyphens.")
        # Check for disallowed name
        if name in settings.DISALLOWED_NAMES:
            raise forms.ValidationError("That name is not allowed.")
        # Check for existing groups
        if Group.objects.filter(name__iexact=name):
            raise forms.ValidationError("That name is already taken.")
        return name
