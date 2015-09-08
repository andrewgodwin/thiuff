# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(height_field=b'height', width_field=b'width', upload_to=b'%Y/%m/%d/')),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
