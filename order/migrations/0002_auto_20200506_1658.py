# Generated by Django 3.0.6 on 2020-05-06 16:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 5, 6, 16, 58, 8, 868805, tzinfo=utc)),
        ),
    ]
