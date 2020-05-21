# Generated by Django 3.0.6 on 2020-05-21 13:49

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20200520_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Category'),
        ),
    ]