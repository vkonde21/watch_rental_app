# Generated by Django 3.0.6 on 2020-05-27 15:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20200527_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date_posted',
            field=models.DateField(default=datetime.datetime(2020, 5, 27, 15, 18, 47, 547080, tzinfo=utc)),
        ),
    ]
