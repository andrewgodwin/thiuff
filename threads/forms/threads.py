from django import forms


class CreateThreadForm(forms.Form):

    title = forms.CharField(
        help_text = "Try for a descriptive title, that lets the user know what they're clicking on."
    )
    url = forms.URLField(
        required = False,
        help_text = "Optional URL to link to. If you don't provide one, all links go to the discussion page."
    )
    body = forms.CharField(
        required = False,
        widget = forms.Textarea,
        label = "Text body",
        help_text = "Optional extra text to show on the discussion page - if you're asking a question or starting a discussion, elaborate here.",
    )
