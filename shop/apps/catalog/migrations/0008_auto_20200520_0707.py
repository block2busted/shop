# Generated by Django 3.0.6 on 2020-05-20 07:07

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_product_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='genre',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Genre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, default='', help_text='Категория', on_delete=django.db.models.deletion.CASCADE, to='catalog.Subcategory'),
        ),
    ]
