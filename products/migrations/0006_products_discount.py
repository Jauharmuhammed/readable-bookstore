# Generated by Django 4.1 on 2022-09-26 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_variation_variation_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='discount',
            field=models.PositiveBigIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]