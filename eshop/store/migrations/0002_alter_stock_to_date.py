# Generated by Django 3.2.15 on 2024-09-14 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 14, 12, 4, 13, 238265)),
        ),
    ]
