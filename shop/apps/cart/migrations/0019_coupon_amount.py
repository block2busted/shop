# Generated by Django 3.0.6 on 2020-06-01 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0018_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
