# Generated by Django 5.1.4 on 2025-04-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0007_shippingaddress_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone',
            field=models.IntegerField(max_length=10),
        ),
    ]
