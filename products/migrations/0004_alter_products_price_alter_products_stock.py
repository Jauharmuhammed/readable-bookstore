# Generated by Django 4.1 on 2022-09-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.PositiveIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='products',
            name='stock',
            field=models.PositiveIntegerField(default=None),
        ),
    ]
