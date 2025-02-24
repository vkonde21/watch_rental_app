# Generated by Django 3.0.6 on 2020-05-05 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_date', models.DateField()),
                ('final_date', models.DateField()),
                ('watch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='product.Product')),
            ],
        ),
    ]
