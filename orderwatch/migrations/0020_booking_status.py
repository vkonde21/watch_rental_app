# Generated by Django 3.0.6 on 2020-05-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderwatch', '0019_booking_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='noorder', max_length=12),
        ),
    ]
