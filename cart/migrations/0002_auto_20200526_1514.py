# Generated by Django 3.0.6 on 2020-05-26 15:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercart',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 26, 15, 14, 15, 513795, tzinfo=utc)),
        ),
    ]
