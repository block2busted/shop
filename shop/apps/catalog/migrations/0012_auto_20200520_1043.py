# Generated by Django 3.0.6 on 2020-05-20 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20200520_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='genre',
            new_name='category',
        ),
    ]