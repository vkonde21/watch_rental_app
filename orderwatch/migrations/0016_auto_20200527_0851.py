# Generated by Django 3.0.6 on 2020-05-27 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orderwatch', '0015_auto_20200527_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderwatch',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 27, 8, 51, 55, 962688, tzinfo=utc)),
        ),
    ]
