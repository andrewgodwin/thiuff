from django import forms
from ..models import Report


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


class ReportForm(forms.Form):
    """
    Form for submitting reports against threads or messages.
    """

    type = forms.ChoiceField(choices=Report.TYPE_CHOICES)
    comment = forms.CharField(widget=forms.Textarea, required=False)
