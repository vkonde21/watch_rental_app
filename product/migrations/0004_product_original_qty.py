# Generated by Django 3.0.6 on 2020-05-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='original_qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
