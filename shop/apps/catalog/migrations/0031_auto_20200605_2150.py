# Generated by Django 3.0.6 on 2020-06-05 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_auto_20200605_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='characteristics',
            new_name='attributes',
        ),
    ]
