# Generated by Django 3.0.6 on 2020-05-27 08:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20200527_0850'),
        ('orderwatch', '0014_auto_20200526_1742'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='booking',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='booking',
            name='cart',
        ),
        migrations.AddField(
            model_name='booking',
            name='bcart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.BookingCart'),
        ),
        migrations.AlterField(
            model_name='orderwatch',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 27, 8, 50, 23, 203666, tzinfo=utc)),
        ),
    ]
