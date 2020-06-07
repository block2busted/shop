# Generated by Django 3.0.6 on 2020-06-07 11:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0035_category_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Характеристики'),
        ),
    ]