# Generated by Django 3.0.6 on 2020-06-01 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_auto_20200601_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
            ],
        ),
    ]
