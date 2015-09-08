from django.contrib import admin
from .models import Image

admin.site.register(
    Image,
    list_display=["id", "image", "created"],
)
