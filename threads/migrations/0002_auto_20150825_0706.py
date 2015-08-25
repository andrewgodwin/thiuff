# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='title',
        ),
        migrations.AddField(
            model_name='group',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='name',
            field=models.CharField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
