# Generated by Django 3.0.6 on 2020-05-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderwatch', '0018_auto_20200527_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
