# Generated by Django 3.0.6 on 2020-05-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Бренд'),
        ),
    ]
