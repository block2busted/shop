# Generated by Django 3.0.6 on 2020-06-07 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_remove_orderproduct_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]