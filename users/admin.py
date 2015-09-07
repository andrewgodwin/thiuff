from django.contrib import admin
from .models import User, UserAuth


admin.site.register(
    User,
    list_display=["id", "username", "created", "is_superuser"],
)


admin.site.register(
    UserAuth,
    list_display=["id", "user", "type", "identifier"],
    raw_id_fields=["user"],
)
