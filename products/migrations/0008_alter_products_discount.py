# Generated by Django 4.1 on 2022-09-29 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_products_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='discount',
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
