# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-29 22:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logReg', '0002_auto_20171029_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friended',
            field=models.ManyToManyField(related_name='_user_friended_+', to='logReg.User'),
        ),
    ]