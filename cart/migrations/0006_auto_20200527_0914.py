# Generated by Django 3.0.6 on 2020-05-27 09:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20200527_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingcart',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 27, 9, 14, 21, 190758, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ordercart',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 27, 9, 14, 21, 188241, tzinfo=utc)),
        ),
    ]
