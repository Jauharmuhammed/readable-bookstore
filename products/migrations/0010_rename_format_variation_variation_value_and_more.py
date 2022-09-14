# Generated by Django 4.1 on 2022-09-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_variation_value_variation_format_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='format',
            new_name='variation_value',
        ),
        migrations.AddField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('format', 'format')], default=None, max_length=100),
            preserve_default=False,
        ),
    ]
