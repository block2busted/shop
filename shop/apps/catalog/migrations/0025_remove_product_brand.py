# Generated by Django 3.0.6 on 2020-05-23 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_auto_20200523_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
    ]