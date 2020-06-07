# Generated by Django 3.0.6 on 2020-06-06 17:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20200606_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, help_text='Характеристики'),
        ),
    ]
