# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 06:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('added_at',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created',)},
        ),
    ]
