# Generated by Django 3.0.6 on 2020-05-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20200512_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
