# Generated by Django 3.0.6 on 2020-05-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_remove_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.TextField(blank=True, default='', verbose_name='Бренд'),
        ),
    ]
