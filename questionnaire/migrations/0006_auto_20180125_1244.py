# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-25 12:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20180124_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='question_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
