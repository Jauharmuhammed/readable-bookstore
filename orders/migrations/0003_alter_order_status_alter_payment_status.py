# Generated by Django 4.1 on 2022-09-18 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Placed', 'Placed'), ('Failed', 'Failed'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Returned', 'Returned'), ('Closed', 'Closed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Failed', 'Failed'), ('Successful', 'Successful')], default='Pending', max_length=100),
        ),
    ]
