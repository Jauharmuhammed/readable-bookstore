# Generated by Django 4.1 on 2022-09-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_remove_orderproduct_status_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupen_discount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='gross_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_charge',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='discount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='gross_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
