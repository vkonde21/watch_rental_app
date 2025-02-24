# Generated by Django 3.0.6 on 2020-05-26 17:42

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20200526_1742'),
        ('cart', '0002_auto_20200526_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='ordercart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cart.OrderCart'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='product.Product'),
        ),
        migrations.AlterField(
            model_name='ordercart',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 26, 17, 42, 39, 234505, tzinfo=utc)),
        ),
    ]
