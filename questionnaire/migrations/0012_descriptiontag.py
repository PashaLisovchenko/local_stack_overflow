# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-01 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('questionnaire', '0011_auto_20180201_0754'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptio', models.TextField()),
                ('tag', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='taggit.Tag')),
            ],
        ),
    ]