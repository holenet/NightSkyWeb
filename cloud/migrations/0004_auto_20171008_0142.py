# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 16:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0003_auto_20171007_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfile',
            old_name='folder',
            new_name='user_folder',
        ),
    ]
