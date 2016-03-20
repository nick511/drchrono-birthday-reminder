# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.IntegerField(default=0)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('chart_id', models.CharField(default='', max_length=10)),
                ('date_of_birth', models.DateTimeField()),
                ('gender', models.CharField(choices=[(None, ''), ('Male', 'Male'), ('Female', 'Female')], max_length=6)),
            ],
        ),
    ]
