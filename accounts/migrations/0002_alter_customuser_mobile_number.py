# Generated by Django 4.1 on 2022-09-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(max_length=10),
        ),
    ]
