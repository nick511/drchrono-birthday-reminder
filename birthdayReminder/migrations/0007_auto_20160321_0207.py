# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthdayReminder', '0006_auto_20160320_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]