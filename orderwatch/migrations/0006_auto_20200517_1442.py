# Generated by Django 3.0.6 on 2020-05-17 14:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orderwatch', '0005_auto_20200516_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderwatch',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 17, 14, 42, 0, 701212, tzinfo=utc)),
        ),
    ]
