# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 14:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secret', '0011_piece_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='piece',
            name='created_at',
        ),
    ]
