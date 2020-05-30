# Generated by Django 3.0.6 on 2020-05-24 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0003_auto_20200524_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]