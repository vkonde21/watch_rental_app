# Generated by Django 3.0.6 on 2020-05-26 17:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orderwatch', '0013_auto_20200526_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderwatch',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 26, 17, 42, 39, 237306, tzinfo=utc)),
        ),
    ]
