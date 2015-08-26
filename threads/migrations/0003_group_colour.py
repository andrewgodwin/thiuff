# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_auto_20150826_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='colour',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
