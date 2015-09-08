# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('threads', '0009_auto_20150905_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='background',
            field=models.ForeignKey(related_name='+', blank=True, to='images.Image', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='logo',
            field=models.ForeignKey(related_name='+', blank=True, to='images.Image', null=True),
        ),
    ]
