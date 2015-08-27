from django.contrib import admin
from .models import Thread, Group, Message

admin.site.register(
    Thread,
    list_display=["id", "title", "author", "created"],
)

admin.site.register(
    Group,
    list_display=["id", "name", "created"],
)

admin.site.register(
    Message,
    list_display=["id", "created"],
)
