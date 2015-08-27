# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_group_colour'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='deleted',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
