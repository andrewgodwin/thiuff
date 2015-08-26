from django import forms


class CreateTopicForm(forms.Form):

    title = forms.CharField()

