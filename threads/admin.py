from django.contrib import admin
from .models import Thread, Group

admin.site.register(
    Thread,
    list_display=["id", "title", "author", "created"],
)

admin.site.register(
    Group,
    list_display=["id", "name", "created"],
)
