# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180131_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_image/default.png', null=True, upload_to='profile_image/'),
        ),
    ]
