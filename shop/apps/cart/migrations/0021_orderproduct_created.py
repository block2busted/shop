# Generated by Django 3.0.6 on 2020-06-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0020_auto_20200605_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=2),
            preserve_default=False,
        ),
    ]