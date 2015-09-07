# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0006_auto_20150904_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='approve_members',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='approve_messages',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='approve_threads',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='frontpage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]
