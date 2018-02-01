# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-01 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0010_auto_20180131_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text_answer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_question',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
