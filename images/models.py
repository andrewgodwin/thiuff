from django.db import models


class Image(models.Model):

    image = models.ImageField(
        upload_to="%Y/%m/%d/",
        height_field="height",
        width_field="width",
    )
    height = models.IntegerField()
    width = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey("users.User")
