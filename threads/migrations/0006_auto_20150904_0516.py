# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0005_auto_20150904_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='num_messages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='num_top_level_messages',
            field=models.IntegerField(default=0),
        ),
    ]
