# Generated by Django 5.1.4 on 2025-05-10 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0011_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
